from flask import Flask, request
from pprint import pprint
import redis, datetime

app = Flask(__name__)
r = redis.StrictRedis()

@app.route('/action', methods=['GET'])
def action_parser():
    _dict = {\
             'class': 'action',
             'ip': str(request.args.get('ip')),
             'type': str(request.args.get('type')),
             'project': str(request.args.get('project')),
             'created_date': str(datetime.datetime.now()),
             'info': str(request.args.get('info'))
            }
    pprint(_dict)
    r.lpush('action', str(_dict))
    r.expire('action', 200)
    return 'OK'


@app.route('/status', methods=['GET'])
def status():
    return str(r.hgetall('today'))


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
