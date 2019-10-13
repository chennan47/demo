function myFunction() {
    param = $('#search').val();
    alert("I am an alert box!");
    if (param != "") {
        $("#status").show();
        var u = 'https://graph.facebook.com/search/?callback=&limit=100&q='+param;
        getResults(u);
        }
}

$(document).ready(function(){
	"use strict";
	var crypto = require('crypto');
    var request = require('request');
    var apiKey = "123";
    var secret="123";
    var timestamp = Math.round((new Date().getTime()/1000));
    var hash = crypto.createHmac('sha512', apiKey+secret+timestamp).digest('hex');
    var authHeaderValue = 'EAN APIKey=' +apiKey+ ',Signature=' + hash + ',timestamp=' + timestamp;
    console.log(crypto);

	//datepicker
    var rangeText = function (start, end) {
        var str = '';
        str += start ? start.format('Do MMMM YYYY') + ' to ' : '';
        str += end ? end.format('Do MMMM YYYY') : '...';

        return str;
    },
    css = function(url){
        var head  = document.getElementsByTagName('head')[0];
        var link  = document.createElement('link');
        link.rel  = 'stylesheet';
        link.type = 'text/css';
        link.href = url;
        head.appendChild(link);
    },
    script = function (url) {
        var s = document.createElement('script');
        s.type = 'text/javascript';
        s.async = true;
        s.src = url;
        var head  = document.getElementsByTagName('head')[0];
        head.appendChild(s);
    }

    var picker = new Lightpick({
        field: document.getElementById('datepicker'),
        singleDate: false,
        onSelect: function(start, end){
            console.log(rangeText(start, end));
        }
    });
    var cars = [
        { "make":"Porsche", "model":"911S" },
        { "make":"Mercedes-Benz", "model":"220SE" },
        { "make":"Jaguar","model": "Mark VII" }
    ];

    function myFunction() {
      // ajax the JSON to the server
//        $.get("location", cars, function(result){
//            console.log(result);
//        });
        console.log('hit');
        fetch('/location', {

        // Specify the method
            method: 'POST',

            // A JSON payload
            body: JSON.stringify({
                "greeting": "Hello from the browser!"
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
            return response.text();
        }).then(function (text) {

            console.log('POST response: ');

            // Should be 'OK' if everything was successful
            console.log(text);
        });
        };
});