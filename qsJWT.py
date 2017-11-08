#!/usr/bin/python3
"""
        Title: Simple JWT authentication for Qlik Sense
        Author: Clint Carr
        Date: 09 November 2017
        Notes: Requires Qlik Sense June 2017 and higher
"""

import jwt
import random
import requests
import string

# create a 16 character xrfkey
characters = string.ascii_letters + string.digits
xrf = ''.join(random.sample(characters, 16))

# Qlik Sense variables
senseHost = 'qmi-qs-cln'
proxyPrefix = 'jwt'
userDirectory = 'jwtSense'
userName = 'testJWT'

# jwt data to send
jwtData = {'userId': userName,
            'userDirectory': userDirectory,
}

# path to the private key used to encrypt the token
privateKeyPath = './certs/private.key'

# open the private key and use it to encrypt the jwtData
with open (privateKeyPath) as pk:
    token = jwt.encode(jwtData, pk.read(), algorithm='RS256')

# set the Qlik Sense headers
headers = {"X-Qlik-XrfKey": xrf,
           "Authorization": "bearer {0}".format(token.decode('UTF-8')),
           "Content-Type": "application/json"}

# use an arbitory endpoint for authentication
endpoint = '/qrs/about'

# send a GET request to the endpoint, I am setting verify to False but you can set this to your root cert
response = requests.get('https://{0}/{1}{2}?xrfkey={3}'.format (senseHost, proxyPrefix, endpoint, xrf),
                                        headers=headers, verify=False)

print (response.content)