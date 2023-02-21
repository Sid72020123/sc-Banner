from API import start_sc, start_sui
from threading import Thread
from flask import Flask

t1 = Thread(target=start_sc)
t2 = Thread(target=start_sui)
t1.start()
t2.start()

app = Flask('app')

@app.route('/')
def hello_world():
  return "I'm Alive!"

app.run(host='0.0.0.0', port=8080)
