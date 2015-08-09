import os

from flask import Flask, request
import requests

import router


JENKINS_URL = os.environ.get('JENKINS_URL', 'http://localhost:8060')
JENKINS_WEBHOOK_URL = '/'.join((JENKINS_URL, 'github-webhook', ''))

app = Flask(__name__)
events = router.EventRouter()


def get_build_url(event_data):
    target_branch_name = event_data['pull_request']['head']['ref']
    repository_name = event_data['repository']['name']
    url_formatter = '{jenkins_url}/job/{repository_name}-{target_branch_name}/build'.format
    return url_formatter(jenkins_url=JENKINS_URL, repository_name=repository_name, target_branch_name=target_branch_name)


@events.register_event('pull_request', repository='*')
def pull_request_handler(event_type, event_data):
    if event_data['action'] != 'closed':
        url = get_build_url(event_data)
        requests.get(url)


@app.route('/github-webhook/', methods=['POST'])
def request_proxy():
    response = requests.post(JENKINS_WEBHOOK_URL, data=request.data, headers=request.headers)
    events.trigger_event_handlers(request.headers['X-GitHub-Event'], request.json)
    return response.content
