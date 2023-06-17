import requests
import random
import json
import re
import os
import io
import upload
import webbrowser
import tkinter
from PIL import ImageTk, Image
from tkinter import Tk, Label, Button, Frame, filedialog
from urllib.parse import urlparse
from os.path import splitext

links = []
current_image = None
current_image_raw = None
current_link = ''
window_width = 900
window_height = 720

# gets the name of a file from an image url
# eg. https://imgur.com/poop.jpeg -> poop.jpeg
def get_filename(url):
    parsed = urlparse(url)
    return os.path.basename(parsed.path)

# resizes an image so that it fits inside our window while maintaining original aspect ratio
def resize_image(img):
	MAX_SIZE = (window_width, window_height - 50)
	img.thumbnail(MAX_SIZE)
	return img

# 
def load_links():
	global links

	# load the links until we have at least one (it's rare, but getting 0 could happen)
	while len(links) == 0:
		# Get a random thread id
		response = requests.get('https://raw.githubusercontent.com/drkinkykinkles/knockout-lmao-pics-ids/master/thread_ids.json')
		list_json = response.json()
		thread_ids = list(list_json.values())
		random_id = random.choice(thread_ids)

		# Get a random page number from the thread
		response = requests.get(f'https://api.knockout.chat/v2/threads/{random_id}/1')
		response_json = response.json()
		last_page = response_json['lastPost']['page']
		random_page = random.randint(1, last_page)

		# Get all posts from the page
		response = requests.get(f'https://api.knockout.chat/v2/threads/{random_id}/{random_page}')
		response_json = response.json()
		posts = response_json['posts']

		# Pull out all media links
		for post in posts:
			content = post['content']
			matches = re.findall(r'(https?:\/\/.*\.(?:png|jpg|jpeg))', content)
			if len(matches) > 0:
				for match in matches:
					if (match not in links): # don't add duplicates
						links.append(match)

# consults the list of links to fetch a new image, returning the Tk image version of it
def get_next_tk_image():
	global links
	global current_image
	global current_link
	global current_image_raw

	succeeded = False
	while not succeeded:
		link = links.pop()
		try:
			response = requests.get(link)
			img = Image.open(io.BytesIO(response.content))
			succeeded = True
		except:
			print(f'couldn\'t load image {link}; skipping to next image')

	current_image = img
	current_link = link
	current_image_raw = response.content
	img = resize_image(img)
	img = ImageTk.PhotoImage(img)

	return img

# handler when clicking "Next" btn; updates the view with the new image
def on_next_image():
	global links
	global image_panel

	# make sure we're topped up on links
	if len(links) == 0:
		load_links()

	img = get_next_tk_image()
	image_panel.configure(image = img)
	image_panel.image = img

# handler when clicking "Save" btn; prompts user to save image
def on_save_image():
	global current_link

	filename = get_filename(current_link)
	file = filedialog.asksaveasfile(mode='wb', initialfile = filename)
	if file:
	    current_image.save(file)
	    print(f'saved image {filename}')

# handler when clicking "Upload" btn; uploads image to postimages.org and then opens img page
def on_upload_image():
	global current_image_raw

	url = upload.upload_image(current_image_raw)
	webbrowser.open_new(url)

# Load the initial list of links
load_links()

# Create our window
root = Tk()
root.title('Endless LMAO Pics')
root.geometry(f'{window_width}x{window_height}+50+50')

# Create the buttons
button_frame = Frame(root)
save_btn = Button(button_frame, text='Save', command = lambda: on_save_image())
save_btn.pack(ipadx=5, ipady=5, side=tkinter.LEFT, fill=tkinter.X, expand=True)

upload_btn = Button(button_frame, text='Upload', command = lambda: on_upload_image())
upload_btn.pack(ipadx=5, ipady=5, side=tkinter.LEFT, fill=tkinter.X, expand=True)

next_btn = Button(button_frame, text='Next >>', command = lambda: on_next_image())
next_btn.pack(ipadx=5, ipady=5, side=tkinter.RIGHT, fill=tkinter.X, expand=True)

# Create the image window
img = get_next_tk_image()
image_panel = Label(root, image = img)

# Add the elements to the root window
button_frame.pack(anchor=tkinter.N, fill=tkinter.X)
image_panel.pack(fill = "both")

root.mainloop()