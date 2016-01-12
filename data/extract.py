#!/usr/bin/env python
from lxml import etree
import lxml.html
import urllib
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

    ul = etree.Element('ul')
    options = document.xpath('//select[@id="meme"]/option')
    for option in options:
        li = etree.Element('li')
        title = etree.Element('div')
        title.text = option.text_content()
        image_url = 'http://apimeme.com/meme?meme=%s' % urllib.quote_plus(title.text)
        image = etree.Element('img', src=image_url, width='300')
        delete = etree.Element('a', href='#', cl='delete')
        delete.text = 'Delete'
        li.append(title)
        li.append(image)
        li.append(delete)
        ul.append(li)
    print etree.tostring(ul, method='html', encoding='utf-8')

if __name__ == '__main__':
    main()

