import google
from googlesamples.assistant.grpc.textinput import SampleTextAssistant
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.transport.grpc import secure_authorized_channel

with open('google_assistant_config.json') as google_assistant_config_file:
    ga_config = json.load(google_assistant_config_file)

with open(ga_config['credentialsFilePath']) as credentials_file:
    grpc_channel_credentials = Credentials(
        token=None,
        **json.load(credentials_file)
    )

http_request = Request()
grpc_channel_credentials.refresh(http_request)

grpc_channel = secure_authorized_channel(
    grpc_channel_credentials, http_request, 'embeddedassistant.googleapis.com')

assistant = SampleTextAssistant("en-US", ga_config['deviceModelID'], ga_config['deviceID'], False,
                                grpc_channel, 60 * 3 + 5)

# Unlocked by default
locked = False


def lock():
    global locked
    if not locked:
        print("Locking!")
        assistant.assist("lock my front door")
        locked = True


def unlock():
    global locked
    if locked:
        print("Unlocking!")
        locked = False
        assistant.assist("unlock my front door")
        assistant.assist(ga_config['lockPIN'])
