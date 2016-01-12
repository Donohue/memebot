import os
import json
import requests
from random import randrange
from flask import Flask, Response, request

app = Flask(__name__)
app.config['DEBUG'] = True

with open('./memes.json') as f:
    memes = json.loads(f.read())

meme_dict = {}
for meme in memes:
    for key in meme['keys']:
        meme_list = meme_dict[key] if key in meme_dict else []
        meme_list.append(meme)
        meme_dict[key] = meme_list

@app.route('/webhook', methods=['POST'])
def webhook():
    meme = None
    meme_key = ''
    for word in request.form.get('text').split():
        meme_key += ' ' + word.lower()
        meme_key = meme_key.strip()
        if meme_key in meme_dict:
            meme_list = meme_dict[meme_key]
            meme = meme_list[randrange(0, len(meme_list))]
    if not meme:
        return 'Memebot failed to find meme for "%s"' % meme_key

    return Response(
        json.dumps({
            'response_type': 'in_channel',
            'attachments': [{
                'text': meme['url'],
                'image_url': meme['url']
            }],
        }),
        mimetype='application/json'
    )

