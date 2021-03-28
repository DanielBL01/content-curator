'''
    parseURL.py

    Takes a url link and uses the newspaper API to parse the content
'''

from newspaper import Article

def curate(url):
    article = Article(url)
    article.download()
    article.parse()

    text = None
    publish_date = None

    try:
        publish_date = article.publish_date
    except: 
        print('Could not find the published Date')

    try:
        text = article.text
    except: 
        print('Could not find the text')

    return text, publish_date