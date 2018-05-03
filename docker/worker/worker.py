import redis, time, os, datetime
from ast import literal_eval
from pprint import pprint


def listen():
    # Listen queue to triage the task
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
                elif action['type'] == 'initialize':
                    initialize(action, r)
                elif action['type'] == 'todayTaskUpdate':
                    todayTaskUpdate(action, r)
                elif action['type'] == 'updateInfo':
                    updateInfo(action, r)
                elif action['type'] == 'shutdownCheck':
                    shutdownCheck(action, r)
            else:
                print 'Sleep 5 seconds'
                time.sleep(5)
        except Exception as e:
            print str(e)


def trigger(action):
    cmd = 'ssh miuser@' + \
            action['ip']+' docker run --rm --name ' + \
            action['project']+' --network host -d python:2 sleep infinity'
    print cmd
    os.system(cmd)
    print 'trigger complete'


def initialize(action, r):
    # Archive yesterday task record
    # Create empty today task
    result = r.hgetall('today')
    if result:
        yesterday_date = (datetime.datetime.today() - datetime.timedelta(1)).strftime("%Y-%m-%d")
        r.hmset(yesterday_date, result)
        r.delete('today')
        r.hmset('today',{'created_date': datetime.datetime.now()})
    else:
        r.delete('today')
        r.hmset('today',{'created_date': datetime.datetime.now()})
    print 'Initialize complete'


def todayTaskUpdate(action, r):
    # Update today project
    result = r.hgetall('today')
    result[action['project']] = {\
                                 'ip': action['ip'],
                                 'boot': 'Pending',
                                 'scan': 'Pending',
                                 'shutdown': 'Pending',
                                }
    r.hmset('today', result)
    print 'todayTaskUpdate complete'


def updateInfo(action, r):
    # Update Success after action like Boot, Scan and shutdown
    result = r.hgetall('today')
    project_result = literal_eval(result[action['project']])
    project_result[action['info']] = 'Success'
    result[action['project']] = project_result
    r.hmset('today',result)
    print action['project'], action['info'], 'Success'


def shutdownCheck(action, r):
    # Check whether the vm is released resource
    result = r.hgetall('today')
    project_result = literal_eval(result[action['project']])
    if project_result['shutdown'] == 'Pending':
        # Force docker to stop
        cmd = 'ssh miuser@' + \
            action['ip']+' docker kill ' + action['project']
        os.system(cmd)
        print 'Force to stop', action['project']
    print 'shutdownCheck complete'


if __name__=='__main__':
    listen()
