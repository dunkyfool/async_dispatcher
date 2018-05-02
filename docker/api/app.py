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
            }
    pprint(_dict)
    r.lpush('action', str(_dict))
    return 'OK'

@app.route('/info', methods=['GET'])
def info_parser():
    _dict = {\
             'class': 'info',
             'ip': str(request.args.get('ip')),
             'type': str(request.args.get('type')),
             'project': str(request.args.get('project')),
             'created_date': str(datetime.datetime.now()),
            }
    pprint(_dict)
    r.lpush('info', str(_dict))
    return 'OK'

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
