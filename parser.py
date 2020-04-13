import requests
import json
from proxy_tool import get_proxy
from dependence import Dependence


class Parser(object):
    def __init__(self):
        self.url = 'https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByGav?_input_charset=utf-8&groupId' \
                   '={}&repoId={}&artifactId={}&version='

    def parse(self, **kwargs):
        artifact_id = kwargs['artifactId']
        group_id = kwargs.get('groupId') or ''
        repo_id = kwargs.get('repo_id') or 'all'
        accurate = kwargs['accurate']
        is_asc = kwargs.get('is_asc', False)
        limit = kwargs['limit'] or 10
        proxy = get_proxy()
        response = requests.get((self.url.format(group_id, repo_id, artifact_id)),
                                proxies={"http": "http://{}".format(proxy)})
        if response.status_code == 200:
            results = json.loads(response.text)['object']
            if accurate:
                dependencies = set(map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']),
                                       filter(lambda item: item['artifactId'] == artifact_id, results)))
            else:
                dependencies = set(
                    map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']), results))

            return sorted(dependencies, key=lambda d: d.version, reverse=not is_asc)[:limit]
