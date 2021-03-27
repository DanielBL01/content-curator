from flask import Flask, render_template
import redis 

app = Flask(__name__)
cache = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/content')
def content():
    return render_template('content.html')

if __name__ == '__main__':
    app.run(debug=True)