import httplib
from collections import namedtuple
import functools
import hashlib
import hmac
import os

from flask import Flask, request
import requests

import router


# Configuration
# ==================================================================================================
JENKINS_URL = os.environ.get('JENKINS_URL', 'http://localhost:8060')
SECRET = os.environ.get('JGHWHP_SECRET')

# Headers
# ==================================================================================================
EVENT_HEADER = 'X-GitHub-Event'
SIGNATURE_HEADER = 'X-Hub-Signature'

# Jenkins
# ====================================================================================================
JENKINS_WEBHOOK_URL = '/'.join((JENKINS_URL, 'github-webhook', ''))


app = Flask(__name__)
events = router.EventRouter()


RequestSignature = namedtuple('RequestDigest', 'algorithm digest')


def compare_digest(a, b):
    """
    Return a == b.

    If python > 2.7.7, uses hmac.compare_digest, otherwise uses `==` comparison.
    """
    if hasattr(hmac, 'compare_digest'):
        return hmac.compare_digest(a, b)
    else:
        return a == b


def with_hmac_verification(app_route):
    """ Decorates app routes with HMAC verification against the configuration secret. """
    @functools.wraps(app_route)
    def wrapper():
        if SECRET is not None:
            header_bytes = bytes(request.headers[SIGNATURE_HEADER])
            signature = RequestSignature(*header_bytes.split('='))
            verification = hmac.new(SECRET, request.data, getattr(hashlib, signature.algorithm))
            assert compare_digest(signature.digest, verification.hexdigest())
        return app_route()
    return wrapper


def generate_build_url(event_data, parameterized_build=False):
    """ Generates the build action URL for the supplied event. """
    target_branch_name = event_data['pull_request']['head']['ref']
    repository_name = event_data['repository']['name']
    url_formatter = '{jenkins_url}/job/{repository_name}-{target_branch_name}/build{build_suffix}'.format
    return url_formatter(jenkins_url=JENKINS_URL,
                         repository_name=repository_name,
                         target_branch_name=target_branch_name,
                         build_suffix='WithParameters' if parameterized_build else '')


@events.register_event('pull_request', repository='*')
def pull_request_handler(event_type, event_data):
    if event_data['action'] != 'closed':
        url = generate_build_url(event_data)
        # Attempt normal build request
        response = requests.post(url)
        # Attempt parameterized build request if normal build request fails
        if response.status_code is not httplib.OK:
            url = generate_build_url(event_data, parameterized_build=True)
            requests.post(url)


@app.route('/webhook/', methods=['POST'])
@with_hmac_verification
def request_proxy():
    response = requests.post(JENKINS_WEBHOOK_URL, data=request.data, headers=request.headers)
    events.trigger_event_handlers(request.headers[EVENT_HEADER], request.json)
    return response.content
