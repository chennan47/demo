#!/usr/bin/env python
from flask import Flask
from settings import base_url, authHeaderValue
from hotel import Hotel
from rooms import Room
import requests
import json

app = Flask(__name__)


class Expedia:

    def __init__(self):
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'Authorization': authHeaderValue,
            'Content-Type': 'application/json',
            'User-Agent': 'Chrome/77.0.3865.120',
        }
        self.base_url = base_url
        self.regions = {
            'New York': '2621',
            'Paris': '2734',
            'London': '2114',
            'Sydney': '178312',
            'Singapore': '3168'
        }
        self.language = {
            'English': 'en-US',
            'Chinese': 'zh-CN'
        }
        self.check_in = ''
        self.check_out = ''
        self.hotels = []
        self.hotel_ids = []
        self.country_code = ''
        self.start = 0
        self.end = 10
        self.region = ''
        self.adults = ''
        self.childs_age = []
        self.rooms_amount = ''
        self.hotels = []
        self.avail_rooms = {}

    def getHotels(self, region, language='Chinese'):
        if region not in self.regions:
            print 'This region is not supported in this demo.'
            return
        if language not in self.language:
            print 'This language is not supported in this demo.'
            return
        self.region = region
        params = {
            'language': self.language[language],
            'include': ['property_ids', 'details']
        }
        res = requests.get(
            url=self.base_url + 'regions/' + self.regions[region],
            headers=self.headers,
            params=params
        )

        self.hotel_ids = list(map(lambda x: x.encode('ascii', 'ignore'), json.loads(res.text)['property_ids']))
        self.country_code = json.loads(res.text)['country_code'].encode('ascii', 'ignore')
        return self.hotel_ids

    def bulck_update_rooms(self, params, start, finish):
        params['property_id'] = self.hotel_ids[start:finish]
        res1 = requests.get(
            url=self.base_url + 'properties/availability',
            headers=self.headers,
            params=params
        )
        all_rooms = json.loads(res1.text)

        for rooms_info in all_rooms:
            property_id = rooms_info['property_id']
            if property_id not in self.avail_rooms:
                self.avail_rooms[property_id] = []
            for data in rooms_info['rooms']:
                if data['rates'][0]:
                    available_nums = data['rates'][0]['available_rooms']
                else:
                    available_nums = 0
                room = Room(
                    id=data['id'],
                    room_name=data['room_name'].encode('ascii', 'ignore'),
                    available_nums=available_nums
                )
                self.avail_rooms[property_id].append(room)
        self.hotel_ids = self.avail_rooms.keys()

    def bulck_update_hotel(self, language, start, finish):
        hotel_infos = self.hotel_ids[start: finish]
        params2 = {
            'language': self.language[language],
            'property_id': hotel_infos,
        }
        res2 = requests.get(
            url=self.base_url + 'properties/content',
            headers=self.headers,
            params=params2
        )

        hotel_res = json.loads(res2.text)
        for hotel_id in hotel_infos:
            hotel = Hotel(
                id=hotel_id,
                name=hotel_res[hotel_id]['chain']['name'].encode('ascii', 'ignore'),
                ratings=hotel_res[hotel_id]['ratings']['property']['rating'].encode('ascii', 'ignore'),
            )
            self.hotels.append(hotel)

    def filter_by_starts(self, ratings):
        ret = []
        for hotel in self.hotels:
            if float(hotel.ratings) >= float(ratings):
                print hotel.name, hotel.ratings, hotel.id
                ret.append(hotel)
        return ret

    def check_available_with_stars(self, region, check_in, check_out, language='Chinese', adults='1',
                                   childs_age=[], rooms_amount='1', ratings=None):
        if self.region != region:
            self.getHotels(region=region, language=language)
        if not (
                self.check_in == check_in and self.check_out == check_out and self.region == region and self.rooms_amount == rooms_amount and self.adults == self.adults):
            self.adults = self.adults
            self.childs_age = childs_age
            self.rooms_amount = rooms_amount
            self.check_in = check_in
            self.check_out = check_out
            if not childs_age:
                occupancy = [adults]
            else:
                occupancy = [adults + '-']
                child = ','.join(childs_age)
                occupancy[0] += child
            if int(rooms_amount) > 1:
                occupancy.append(rooms_amount)
            params = {
                'language': self.language[language],
                'checkin': self.check_in,
                'checkout': self.check_out,
                'currency': 'USD',
                'country_code': self.country_code,
                'sales_channel': 'website',
                'sales_environment': 'hotel_only',
                'sort_type': 'preferred',
                'rate_plan_count': 1,
                'occupancy': occupancy
            }

            # bulck request for all rooms api limits 250
            i = 0
            while i + 200 < len(self.hotel_ids):
                self.bulck_update_rooms(params, i, i + 200)
            self.bulck_update_rooms(params, i, len(self.hotel_ids))
            self.hotel_ids = self.avail_rooms.keys()

            j = 0
            while i + 200 < len(self.hotel_ids):
                self.bulck_update_hotel(language, i, i + 200)
            self.bulck_update_hotel(language, i, len(self.hotel_ids))

            if ratings:
                self.filter_by_starts(ratings)

    def display_rooms(self, hotel_id):
        hotel_name = ''
        hotel_ratings = ''
        for hotel in self.hotels:
            if hotel.id == hotel_id:
                hotel_name = hotel.name
                hotel_ratings = hotel.ratings
        ret = ['hotel name:{}\nhotel ratings:{}\n'.format(hotel_name, hotel_ratings)]
        rooms = self.avail_rooms[hotel_id]
        for room in rooms:
            room_name = room.room_name
            left = str(room.available_nums)
            nw_info = 'room name:{} available numble:{}\n'.format(room_name, left)
            if nw_info not in ret:
                ret.append(nw_info)
        ans = ''.join(ret)
        print ans