from API import start
from threading import Thread
from flask import Flask

t = Thread(target=start)
t.start()

app = Flask('app')

@app.route('/')
def hello_world():
  return "I'm Alive!"

app.run(host='0.0.0.0', port=8080)
