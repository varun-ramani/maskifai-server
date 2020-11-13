# maskifai-server
This repository contains the code for the backend of Maskif.ai, the AI-powered smart lock.
See Maskif.ai client repo here: https://github.com/varun-ramani/maskifai-client

# Motivation
As businesses around the world begin to reopen, many of them have issued mandatory
mask mandates to protect the safety of their employees and customers. Unfortunately, where there
are rules, there are people who decide not to follow them. As of today, there have been countless incidents
of people arguing with business owners over the importance of wearing a mask. This is not only disrespectful and
a waste of time for these business owners, but it is also dangerous given the pandemic.
How can we solve this issue? 

# What we built
Introducing Maskif.ai, the AI-powered smart lock. Maskif.ai uses computer vision to detect 
people who are not wearing a mask and then subsequently locks the door to keep them out. Maskif.ai
is compatible with Google Home, and thus can be used with a multitude of smart devices. Here is a 
video which includes a demo and some more information about what Maskif.ai does: https://www.youtube.com/watch?v=EG8_0GUnhqg&feature=youtu.be

# How it works
This repository communicates with a mobile app that's hosted in the Maskif.ai client repo (link above)
to stream video input into a classifier using websockets. Once the video input has reached the classifier,
it determines whether or not a given person is wearing a mask. If the person is not wearing a mask, then 
the smart lock activates and locks the person out.

# Using Maskifai
- Clone this repo using: ```git clone github.com/varun-ramani/maskifai-server```
- Install dependencies using: ```pip install -r requirements.txt```
- Set up google home sdk by following directions on website: https://developers.google.com/assistant/sdk
- Create ```google_assistant_config.json``` and fill it with the following info <br> 
```
{
        "credentialsFilePath": "<path to credentials.json>"
        "deviceID": "<google assistant device ID>"
        "deviceModelID: "<the model id sourced from the google assistant>"
        "lockPIN": "<PIN you set in the Google Home app to unlock your door>"
}
```
- Add a smart lock to your Google Home app 
-  Launch server using: ```python main.py```
<br>
<br>
If you just want to test the classifier, simply run test.py

# Devpost
Check out our devpost at: https://devpost.com/software/maskif-ai.
This project was created as part of YHack 2020
