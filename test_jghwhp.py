import json
import mock

from jghwhp import proxy


class TestPullRequestEvents(object):
    def setup(self):
        self.event_data = {
            'pull_request': {
                'head': {'ref': 'feature-branch' },},
            'repository': {
                'name': 'testrepository',
                'full_name': 'testorg/testrepository',
            },
        }

    @mock.patch('jghwhp.proxy.requests')
    def test_proxy_closed_pull_request(self, patched_requests):
        response = mock.Mock(name='response', content='test data', status_code=200)
        patched_requests.post.return_value = response
        with proxy.app.test_client() as client:
            self.event_data['action'] = 'closed'
            response = client.post('/github-webhook/',
                                   headers={'X-GitHub-Event': 'pull_request',
                                            'Content-Type': 'application/json'},
                                   data=json.dumps(self.event_data))
            assert response.status_code == 200
            assert response.data == 'test data'
            assert not patched_requests.get.called

    @mock.patch('jghwhp.proxy.requests')
    def test_proxy_opened_pull_request(self, patched_requests):
        response = mock.Mock(name='response', content='test data', status_code=200)
        patched_requests.post.return_value = response
        with proxy.app.test_client() as client:
            self.event_data['action'] = 'opened'
            response = client.post('/github-webhook/',
                                   headers={'X-GitHub-Event': 'pull_request',
                                            'Content-Type': 'application/json'},
                                   data=json.dumps(self.event_data))
            assert response.status_code == 200
            assert response.data == 'test data'
            assert patched_requests.get.called

    @mock.patch('jghwhp.proxy.requests')
    def test_proxy_reopened_pull_request(self, patched_requests):
        response = mock.Mock(name='response', content='test data', status_code=200)
        patched_requests.post.return_value = response
        with proxy.app.test_client() as client:
            self.event_data['action'] = 'reopened'
            response = client.post('/github-webhook/',
                                   headers={'X-GitHub-Event': 'pull_request',
                                            'Content-Type': 'application/json'},
                                   data=json.dumps(self.event_data))
            assert response.status_code == 200
            assert response.data == 'test data'
            assert patched_requests.get.called

    @mock.patch('jghwhp.proxy.requests')
    def test_url_formatting(self, patched_requests):
        expected_url = 'http://localhost:8060/job/{repository_name}-{target_branch_name}/build'.format(
            repository_name=self.event_data['repository']['name'],
            target_branch_name=self.event_data['pull_request']['head']['ref'],
        )
        actual_url = proxy.generate_build_url(self.event_data)
        assert expected_url == actual_url
