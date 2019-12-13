from flask import Flask, request, make_response, jsonify, abort
import sys
from datetime import date
import re
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

restService = Flask(__name__)

authenticator = IAMAuthenticator(os.environ["API_KEY"])
assistant = AssistantV2(
    version='2019-02-28',
    authenticator = authenticator
)
assistant.set_service_url(os.environ["WATSON_URL"])

def asJsonResponse(data):
    return make_response(jsonify(data))

@restService.route("/")
def default():
    return "The REST service is up"

@restService.route("/watson/session", methods=['GET'])
def watson():

    response = assistant.create_session(
        assistant_id=os.environ["ASSISTANT_ID"]
    ).get_result()

    print(json.dumps(response, indent=2))

    return asJsonResponse(response)


@restService.route("/watson/message/send", methods=['POST'])
def sendMessage():
    req = request.get_json(force=True)

    sessionId = req.get('sessionId')
    message = req.get('message')

    response = assistant.message(
        assistant_id=os.environ["ASSISTANT_ID"],
        session_id=sessionId,
        input={
            'message_type': 'text',
            'text': message
        }
    ).get_result()

    #print(response.get("output").get("generic")[0].get("text"))

    return asJsonResponse(response)

