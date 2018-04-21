import redis, time
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
            else:
                print 'Sleep 5 seconds'
                time.sleep(5)
        except Exception as e:
            print str(e)


def boot():
    pass


def shutdown():
    pass


def trigger():
    pass


def alert():
    pass


if __name__=='__main__':
    listen()
