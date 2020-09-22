import simplejson
import requests
from collections import Counter
import json 

response = requests.get('https://api.imgflip.com/get_memes')
data = response.json()
# print(type(data))

memesObj = data['data']['memes']

memesList = []
for index,data in enumerate(memesObj):
	memesList.append(data)
	print(index,data)
	if index==4:
		break



