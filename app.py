from flask import Flask, session, render_template, request, redirect, url_for
from utils import curateURL, summarizeText
import redis 

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        return redirect(url_for('content', url=request.form['url']))

    return render_template('homepage.html')

@app.route('/content')
def content():
    url = request.args['url']
    if cache.exists(url):
        summary = cache.hmget(url, 'summary')
        date = cache.hmget(url, 'date')
        print('Retrieve from Cache')
        return render_template('content.html', summary = summary.decode('utf-8'), date = date.decode('utf-8'))
    
    text, date = curateURL.curate(url)
    print(text)
    print(date)
    if text is None and date is None:
        return render_template('error.html')
    elif text is None:
        date = date.strftime('%m/%d/%Y, %H:%M:%S')
        cache.hset(url, 'summary', 'Could not find text information.')
        cache.hset(url, 'date', date)
        return render_template('content.html', summary = 'Could not find text information', date = date)
    elif date is None:
        summary = summarizeText.summarize(text)
        cache.hset(url, 'summary', summary)
        cache.hset(url, 'date', 'Could not find the publish date')
        return render_template('content.html', summary = summary, date = 'Could not find the publish date.')

    summary = summarizeText.summarize(text)
    date = date.strftime('%m/%d/%Y, %H:%M:%S')
    print('Retrieve from curateURL.py')
    cache.hset(url, 'summary', summary)
    cache.hset(url, 'date', date)

    return render_template('content.html', summary = summary, date = date)

if __name__ == '__main__':
    app.run(debug=True)