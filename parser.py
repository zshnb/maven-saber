import requests
import json
from proxy_tool import get_proxy
from dependence import Dependence


class Parser(object):
    def __init__(self):
        self.url = 'https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByWords?_input_charset=utf-8' \
                   '&queryTerm={}&repoId={}'

    def parse(self, **kwargs):
        keyword = kwargs['keyword']
        repo_id = kwargs.get('repo_id', 'all')
        accurate = kwargs['accurate']
        is_asc = kwargs.get('is_asc', False)
        proxy = get_proxy()['proxy']
        dependencies = set()
        response = requests.get((self.url.format(keyword, repo_id)), proxies={"http": "http://{}".format(proxy)})
        if response.status_code == 200:
            results = json.loads(response.text)['object']
            if accurate:
                dependencies = set(map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']),
                                       filter(lambda item: item['artifactId'] == keyword, results)))
            else:
                dependencies = set(
                    map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']), results))

            return sorted(dependencies, key=lambda d: d.version, reverse=not is_asc)
