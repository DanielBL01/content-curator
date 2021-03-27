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
    content = parseURL.parse(request.args['url'])
    if content == '':
        return render_template('error.html')
    
    summary = contentCurator.summerize(content)
    return render_template('content.html', content=content, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)