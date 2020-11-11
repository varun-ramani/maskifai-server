import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2, embedded_assistant_pb2_grpc
)

# Unlocked by default
locked = False

def lock():
    global locked
    if not locked:
        print("Locking!")
        locked = True

def unlock():
    global locked
    if locked:
        print("Unlocking!")
        locked = False