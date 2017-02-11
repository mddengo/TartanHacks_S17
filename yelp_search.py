import io
import json

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1

with io.open('yelp-secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

term = 'chicken'

def searchFood(term, limit = 5, sort = 2, radius_filter = 8000): #sort = 2 is for highested rated
    params = {'term':term, 'limit':limit, 'sort':sort, 'radius_filter':radius_filter, 'lang':'fr'}
    result = client.search('Pittsburgh', **params)
    businesses = result.businesses
    names = ""
    for i in range(0,limit):
        if i == limit-1:
            names += "and " + businesses[i].name
        else:
            names += businesses[i].name + ", "
    return names

recs = searchFood('chicken')

text_to_speech = TextToSpeechV1(
    username='573eea08-b036-476e-8701-ba6afe44e12a',
    password='5qir686Ar1sz',
    x_watson_learning_opt_out=True)  # Optional flag

print(json.dumps(text_to_speech.voices(), indent=2))

with open(join(dirname(__file__), '../recommendations.wav'),
          'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize('Some good' + term + 'places are, ' + recs, accept='audio/wav',
                                  voice="en-US_AllisonVoice"))

print(
    json.dumps(text_to_speech.pronunciation(
        'Watson', pronunciation_format='spr'), indent=2))

print(json.dumps(text_to_speech.customizations(), indent=2))