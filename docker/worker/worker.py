import redis, time, os
from ast import literal_eval
from pprint import pprint


def listen():
    r = redis.StrictRedis()
    while True:
        try:
            queue_len = r.llen('action')
            print queue_len
            if queue_len > 0:
                action = literal_eval(r.rpop('action'))
                pprint(action)
                if action['type'] == 'trigger':
                    trigger(action)
                elif action['type'] == 'check_status':
                    check_status(action)
            else:
                print 'Sleep 5 seconds'
                time.sleep(5)
        except Exception as e:
            print str(e)


def trigger(action):
    cmd = 'ssh miuser@' + \
            action['ip']+' docker run --rm --name ' + \
            action['project']+' --network host -d worker:alpha'
    os.system(cmd)


def check_status(action):
    pass


if __name__=='__main__':
    listen()
