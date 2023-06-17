import requests

def upload_image(img):
	url = 'https://postimg.cc/json'
	files = {'file': img}

	params = {
		'token': '61aa06d6116f7331ad7b2ba9c7fb707ec9b182e8',
		"upload_session": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		"numfiles": "1"
	}
	response = requests.post(url, files=files, data=params)

	if response.status_code == requests.codes.ok:
		json = response.json()
		print(f'Find the image at: {json["url"]}')
		return json['url']
	else:
		print('Error uploading the image to postimages.org')
		print(response.status_code)