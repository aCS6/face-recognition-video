import requests
response = requests.get("http://192.168.1.100:2023/node/face")
# print(response.json())

image_list = []
name_list = []

for i in response.json():
	image_list.append(i['imgfile'])
	name_list.append(i['name'])

print(image_list)
print(name_list)