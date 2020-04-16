import requests
import json
from proxy_tool import get_proxy
from dependence import Dependence


class Parser(object):
    def __init__(self):
        self.url = 'https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByGav?_input_charset=utf-8&groupId' \
                   '={}&repoId={}&artifactId={}&version='
        self.repo = dict()
        self.repo['aliyun'] = self.aliyun
        self.repo['sonatype'] = self.sonatype

    def parse(self, **kwargs):
        repo_id = kwargs.get('repo_id') or 'sonatype'
        proxy = get_proxy()
        dependencies = self.repo[repo_id](proxy,
                                          artifact_id=kwargs['artifact_id'],
                                          accurate=kwargs['accurate'],
                                          is_asc=kwargs['is_asc'],
                                          limit=kwargs['limit'] or 5)
        return dependencies

    def aliyun(self, proxy, **kwargs):
        artifact_id = kwargs['artifactId']
        accurate = kwargs['accurate']
        is_asc = kwargs['is_asc']
        limit = kwargs['limit'] or 5
        url = 'https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByGav?_input_charset=utf-8&groupId' \
              '=&repoId=all&artifactId={}&version='
        response = requests.get((url.format(artifact_id)),
                                proxies={"http": "http://{}".format(proxy)})
        dependencies = set()
        if accurate:
            dependencies = set(map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']),
                                   filter(lambda item: item['artifactId'] == artifact_id,
                                          json.loads(response.text)['object'])))
        else:
            dependencies = set(map(lambda item: Dependence(item['artifactId'], item['groupId'], item['version']),
                                   json.loads(response.text)['object']))

        dependencies = sorted(dependencies, key=lambda d: d.version, reverse=not is_asc)
        if len(dependencies) < limit:
            return dependencies
        else:
            return dependencies[:limit]

    def sonatype(self, proxy, **kwargs):
        artifact_id = kwargs['artifact_id']
        accurate = kwargs['accurate']
        is_asc = kwargs['is_asc']
        limit = kwargs['limit'] or 5
        url = 'https://search.maven.org/solrsearch/select?q={}&start=0&rows=20'
        response = requests.get((url.format(artifact_id)),
                                proxies={"http": "http://{}".format(proxy)})
        dependencies = set()
        if accurate:
            dependencies = set(map(lambda item: Dependence(item['a'], item['g'], item['latestVersion']),
                                   filter(lambda item: item['a'] == artifact_id,
                                          json.loads(response.text)['response']['docs'])))
        else:
            dependencies = set(map(lambda item: Dependence(item['a'], item['g'], item['latestVersion']),
                                   json.loads(response.text)['response']['docs']))

        dependencies = sorted(dependencies, key=lambda d: d.version, reverse=not is_asc)
        if len(dependencies) < limit:
            return dependencies
        else:
            return dependencies[:limit]
