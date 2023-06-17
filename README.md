# Overview

## thread_ids.json
A list of thread ids for the Knockout.chat LMAO Pics threads. Starts at v60.

To be used with the LMAO Pics iOS Shortcuts seen [**here**](https://knockout.chat/thread/33438).

## viewer program
A simple python program that pulls random images from the LMAO threads and displays them. You then have the option to save the image or upload it to postimages.org.

### Prerequisites
You checked the box to install tkinter when you installed Python. If you didn't do this, rerun the installer and modify your installation.

### How to use
Run the following:
```
pip install requests
pip install pillow
py endless_pics.py
```

### Notes
I made this so I could browse random LMAO pics and then take the ones I find particularly funny and post them to Squabbles.io. Maybe eventually I'll get automatic Squabbles post creating hooked up. For now, you'll have to make the post yourself.

While the image uploading may seem redundant (why not just post the image urls from Knockout to Squabbles?) I do this because imgur appears to rate limit the site sometimes. So I said screw it and I just upload the image to postimages.org to avoid this issue no matter who hosted the image originally.