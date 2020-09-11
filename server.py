from flask import Flask, request, abort
import time



app = Flask(__name__)
db =[]

@app.route("/")
def hello():
    return "Добро пожаловать на сервер нашего мессенджера <a href='/status'>Статус </a>"

def find_user(db):
    users = set()
    for message in db:
        users.add(message['name'])
    return list(users)

@app.route("/status")
def status():
    return {'status': True,
            'name':'Messenger',
            'users':find_user(db),
            'messages':len(db),
            'time': time.asctime()}


@app.route("/send", methods= ['POST'])
def send():
    data = request.json
    timestamp = time.time()
    db.append({
        'id': len(db),
        'name': data['name'],
        'text': data['text'],
        'timestamp': timestamp
    })
    return {'ok':True}

@app.route("/messages")
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit>max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit

    after_id=0
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        else:
            after_id +=1


    return {'messages' : db[after_id:after_id+limit]}

app.run()