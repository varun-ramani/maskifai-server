import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2, embedded_assistant_pb2_grpc
)

def lock():
    print("Locking!")

def unlock():
    print("Unlocking!")