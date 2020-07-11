# API accessing Geo Coder API
# Purpose is to extract Coordinates for inout address.
# Ervin Centeno

import requests
import json
import string
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

global body

replay = 'y'
while replay == 'y':
    # Long and Lat Request for Address.
    while True:
        try:
            address = input('Please enter an address along with the city, state, and zip code:\n')

            r = requests.get('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address='
                             + address + '&benchmark=9&format=json')

            data = r.json()
            longitude = data['result']['addressMatches'][0]['coordinates']['x']
            latitude = data['result']['addressMatches'][0]['coordinates']['y']
            break
        except IndexError:
            print('Try again')
            continue

    # Dark Sky API Request.
    fr = requests.get('https://api.darksky.net/forecast/66b058fe292988f7486dcbb4b45da132/' + str(latitude) + ','
                      + str(longitude))
    fdata = fr.json()
    body = ''
    for i in range(7):

        timestamp = fdata['daily']['data'][i]['time']
        date = datetime.fromtimestamp(timestamp)
        current = fdata['daily']['data'][i]['icon']
        if current == ('rain' or 'snow' or 'sleet'):
            print(date.strftime("%x: %A"), ' - ', u'\u2602')
            body = body + str((date.strftime("%x: %A") + '-' + u'\u2602\n'))
        else:
            print(date.strftime("%x: %A"), ' - ', u'\u2600')
            body = body + str((date.strftime("%x: %A") + '-' + u'\u2600\n'))
        i = i + 1

    replay = input("Would you like to try another address? (y/n)\n")
    if replay != 'y':
        break

# Loop to send a text message.
sms = input("would you like to send an SMS?(y/n)\n")
while sms == 'y':
    if sms == 'y':
        acc_sid = 'AC13bbf0ed7ae558e35a7d16308bcea336'
        auth_token = '4321fca416380a9e0e9cfc2d5815d914'
        client = Client(acc_sid, auth_token)

        while True:
            try:
                phone_num = input('Enter a the phone number you want to send to:\n')

                message = client.messages \
                    .create(from_='+17323380784',
                            body='Here is the forcast:\n ' + body,
                            to='+1' + phone_num)
                print('Message sent.')
                sms = input('Would you like to send the forecast to another number? (y/n)\n')
                if sms != 'y':
                    break

            except TwilioRestException as e:
                if e.code == 20404:
                    break
    else:
        print('Thank you!')
        break
