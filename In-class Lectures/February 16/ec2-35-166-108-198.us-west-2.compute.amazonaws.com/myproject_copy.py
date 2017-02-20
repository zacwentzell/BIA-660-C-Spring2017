import os
import json
import requests
from flask import Flask, request, Response
from textblob import TextBlob
# be sure to install TextBlob, see the talk_to_your_server.ipynb


application = Flask(__name__)

#SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

slack_inbound_url = 'https://hooks.slack.com/services/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'

@application.route('/slack', methods=['POST'])
def inbound():
    response = {'username': 'zac_bot', 'icon_emoji': ':robot_face:'}
    #if request.form.get('token') == SLACK_WEBHOOK_SECRET:
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    inbound_message = username + " in " + channel + " says: " + text
    if username in ['zac.wentzell', 'yangyang729'] and 'zac_bot_respond' in text:
	response = {'text': 'Hey {}, I hear you'.format(username), 'icon_emoji': ':robot_face:', 'username': 'zac_bot'}
	r = requests.post(slack_inbound_url, json=response)
	print r.text
    elif username != 'zac_bot' and text.startswith('analyze_sentiment:'):
	response['text'] = 'Analyzing Sentiment:\n{}'.format(str(TextBlob(text[text.find(':')+1:]).sentiment))
	r = requests.post(slack_inbound_url, json=response)
	print r.text
    print inbound_message
    print request.form
    print '\n\n'
    print request.headers
    print request.data
    print request.url
    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)

