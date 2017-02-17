import os
import json
import requests
from flask import Flask, request, Response
from textblob import TextBlob


app = Flask(__name__)

#SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

slack_inbound_url = 'https://hooks.slack.com/services/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'

@app.route('/slack', methods=['POST'])
def inbound():
    response = {'username': 'zac_bot', 'icon_emoji': ':robot_face:'}
    #if request.form.get('token') == SLACK_WEBHOOK_SECRET:
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    inbound_message = username + " in " + channel + " says: " + text
    if username in ['zac.wentzell']:
        response['text'] = 'Hey dude!'

        r = requests.post(slack_inbound_url, json=response)

    print inbound_message
    print request.form

    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=41953)

