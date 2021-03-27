'''
    parseURL.py

    Takes a url link and uses the newspaper API to parse the content
'''

from newspaper import Article

def parse(url):
    article = Article(url)
    article.download()
    article.parse()
    
    return article.text