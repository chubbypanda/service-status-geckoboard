# assingement for Geckoboard's Support Engineer Coding Challenge, by k., 2016/10/14
# https://gist.github.com/luise64/931fcded2801c27f7d3d5b6792815444


import requests
import time
from threading import Timer

# GitHub API details from https://status.github.com/api
github_api = 'https://status.github.com/api/status.json'
# Twilio API details at https://status.twilio.com/api
twilio_api = 'https://gpkpyklzq55q.statuspage.io/api/v2/status.json'

def api_poll(api_url):
    """polling a message in JSON format from the service's API
    """
    return requests.get(api_url).json()

def github_status():
    """returns an integer (1 if the service status is sound, 0 once down)
    """
    service_status = 0
    if api_poll(github_api)['status'] == 'good':
        service_status = 1
    return service_status

def twilio_status():
    """returns an integer (1 if the service status is sound, 0 once down)
    """
    service_status = 0
    if api_poll(twilio_api)['status']['description'] == 'All Systems Operational':
        service_status = 1
    return service_status


# Geckoboard overview and API details
# https://developer.geckoboard.com/getting-started
# https://developer-custom.geckoboard.com/#bar-chart

# assigned API Key (to be found in: user icon - Account - Account Details)
api_key = 'c35ed13a7d3fd2239cfc81a9a4b54f67'

def availability_check():
    # using service API key as authentication
    availability = requests.get('https://api.geckoboard.com', auth=(api_key, ''))
    # dataset API accepts secure connections only, expected to get a 200 response containing {}
    if availability.status_code != 200:
        print 'Your API key is probably incorrect, server response:', availability.status_code

def create_dataset():
    """follows dataset structure defined in
       https://developer.geckoboard.com/api-reference/curl/#create
    """
    # string after the last / identifies the dataset from within the application, e.g. 'example'
    requests.put('https://api.geckoboard.com/datasets/example', json={
                 'fields': {
                   'availibility': {
                     'type': 'number',
                     'name': 'Availibility'
                   },
                   'service': {
                     'type': 'string',
                     'name': 'Service'
                   }
                  }
                }, auth=(api_key, ''))

def delete_dataset():
    """ deletes dataset named 'example', to be used manually only
    """
    requests.delete('https://api.geckoboard.com/datasets/example', auth=(api_key, ''))

def update_dataset():
    """follows dataset update procedure from
       https://developer.geckoboard.com/api-reference/curl/#replace
    """
    # string after the last / identifies the dataset data, e.g. 'example/data'
    requests.put('https://api.geckoboard.com/datasets/example/data', json={
                 'data': [
                    {
                      'service': 'GitHub',
                      'availibility': github_status()
                    },
                    {
                      'service': 'Twilio',
                      'availibility': twilio_status()
                    }
                 ]
                }, auth=(api_key, ''))


def main_thread():
    """run a function every 5 minutes (5 * 60 seconds)
       usage of threading.Timer class suggested by https://docs.python.org/2.7/library/sched.html
    """
    time_interval = 5 * 60
    print 'polling & pushing every 5 minutes...'
    api_push = Timer(time_interval, main_thread, ())
    api_push.start()
    print 'GitHub:', api_poll(github_api)['status'], api_poll(github_api)['last_updated']
    print 'Twilio:', api_poll(twilio_api)['status']['description'], api_poll(twilio_api)['page']['updated_at']
    update_dataset()
    print 'to quit the polling & pushing tasks please press <Ctrl>+<F6>\n'
    # sleep while time-delay events execute; avoid sliding time window after each call
    time.sleep(time_interval - time.time() % time_interval)
    

availability_check()
create_dataset()
main_thread()
