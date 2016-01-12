# -*- coding: utf-8 -*-
import os
import json
import requests
import re
import urllib
import urlparse
from random import randrange
from flask import Flask, Response, request

app = Flask(__name__)
app.config['DEBUG'] = True

SLACK_CLIENT_ID = os.environ['SLACK_CLIENT_ID']
SLACK_CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']

with open('./memes.json') as f:
    memes = json.loads(f.read())

meme_dict = {}
for meme in memes:
    for key in meme['keys']:
        meme_list = meme_dict[key] if key in meme_dict else []
        meme_list.append(meme)
        meme_dict[key] = meme_list

def get_meme_and_other_words(text):
    meme = None
    meme_key = ''
    other_words = []
    for word in text.split():
        meme_key += ' ' + word.lower()
        meme_key = meme_key.strip()
        if meme:
            other_words.append(word)
        elif meme_key in meme_dict:
            meme_list = meme_dict[meme_key]
            meme = meme_list[randrange(0, len(meme_list))]
    return meme, other_words

def get_url_for_meme(meme, other_words):
    url = meme['url']
    if not 'apimeme' in meme or len(other_words) < 2:
        return url

    top = ''
    bottom = ''
    other_string = ' '.join(other_words).encode('utf-8')
    other_string = other_string.replace('“', '"').replace('”', '"')
    matches = re.findall(r'\"(.+?)\"', other_string)
    if len(matches) >= 2:
        top = matches[0]
        bottom = matches[1]
    elif len(matches):
        bottom = matches[0]
    parts = list(urlparse.urlparse(url))
    query_dict = dict(urlparse.parse_qsl(parts[4]))
    query_dict.update({
        'top': top,
        'bottom': bottom
    })
    parts[4] = urllib.urlencode(query_dict)
    return urlparse.urlunparse(parts)

@app.route('/webhook', methods=['POST'])
def webhook():
    meme, other_words = get_meme_and_other_words(request.form.get('text'))
    if not meme:
        return 'Memebot failed to find meme for "%s"' % meme_key
    url = get_url_for_meme(meme, other_words)
    return Response(
        json.dumps({
            'response_type': 'in_channel',
            'attachments': [{
                'text': url,
                'image_url': url
            }],
        }),
        mimetype='application/json'
    )

@app.route('/oauth', methods=['GET'])
def oauth():
    code = request.args.get('code')
    if not code:
        return 'Failure'

    params = {
        'client_id': SLACK_CLIENT_ID,
        'client_secret': SLACK_CLIENT_SECRET,
        'code': code
    }
    print params
    try:
        response = requests.post('https://slack.com/api/oauth.access', data=params)
        print response.text
    except Exception, e:
        return 'Slack request failed: %s' % str(e)
    return 'Success'
