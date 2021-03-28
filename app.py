from flask import Flask, session, render_template, request, redirect, url_for
from utils import parseURL, contentCurator
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
        summary = cache.get(url)
        print('Getting summary from cache')
        return render_template('content.html', summary = summary.decode('utf-8'))
    
    content = parseURL.parse(url)
    if content == '':
        return render_template('error.html')

    summary = contentCurator.summerize(content)
    print('Getting summary with contentCurator.py')
    cache.set(url, summary)

    return render_template('content.html', summary = summary)

if __name__ == '__main__':
    app.run(debug=True)