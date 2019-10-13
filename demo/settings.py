#!/usr/bin/env python
import hashlib
import time
apiKey = "1m6lfng9fqd5fkv57r1c0cms70"
secret = "60mdjb6pisd5u"
timestamp = str(int(time.time()))
authHeaderValue = "EAN APIKey=" + apiKey + ",Signature=" + hashlib.sha512(apiKey+secret+timestamp).hexdigest() + ",timestamp=" + timestamp
base_url = 'https://test.ean.com/2.3/'