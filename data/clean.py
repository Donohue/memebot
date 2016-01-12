#!/usr/bin/env python
import urllib
import lxml.html
import json
import sys

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s <apimeme.com HTML file>'
        sys.exit(-1)
    try:
        f = open(sys.argv[1])
        parser = lxml.html.HTMLParser(encoding='utf-8')
        document = lxml.html.document_fromstring(f.read(), parser=parser)
    except Exception, e:
        print 'Failed to read file: %s' % str(e)
        sys.exit(-1)

    memes = []
    for li in document.xpath('//li'):
        div = li.xpath('./div')[0]
        title = div.text_content().lower()
        apimeme = div.text_content()
        memes.append({
            'title': title,
            'keys': [title],
            'url': 'http://apimeme.com/meme?meme=%s&top=&bottom=' % urllib.quote_plus(apimeme),
            'apimeme': apimeme
        })
    print json.dumps(memes, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()

