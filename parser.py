import requests
import json
from proxy_tool import get_proxy
from dependence import Dependence
from bs4 import BeautifulSoup
from nexus_config import nexus_repo


class Parser(object):
    def __init__(self):
        self.repo = dict()
        self.repo['aliyun'] = self.aliyun
        self.repo['sonatype'] = self.sonatype
        self.repo['mvn'] = self.mvn_central
        self.repo['nexus'] = self.nexus

    def parse(self, **kwargs):
        repo_id = kwargs.get('repo_id') or 'sonatype'
        proxy = get_proxy()
        if repo_id in nexus_repo.keys():
            dependencies = self.repo['nexus'](proxy, nexus_repo[repo_id], artifact_id=kwargs['artifact_id'],
                                              accurate=kwargs['accurate'])
        else:
            dependencies = self.repo[repo_id](proxy, artifact_id=kwargs['artifact_id'],
                                              accurate=kwargs['accurate'])
        group_id = kwargs['group_id']
        is_asc = kwargs['is_asc']
        limit = kwargs['limit'] or 5

        if group_id is not None:
            dependencies = [d for d in dependencies if d.group_id == group_id]

        dependencies = sorted(dependencies, key=lambda d: d.version, reverse=not is_asc)
        if len(dependencies) < limit:
            return dependencies
        else:
            return dependencies[:limit]

    def aliyun(self, proxy, **kwargs):
        artifact_id = kwargs['artifactId']
        accurate = kwargs['accurate']
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
        return dependencies

    def sonatype(self, proxy, **kwargs):
        artifact_id = kwargs['artifact_id']
        accurate = kwargs['accurate']
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

        return dependencies

    def mvn_central(self, proxy, **kwargs):
        artifact_id = kwargs['artifact_id']
        url = 'https://mvnrepository.com/search?q={}'
        response = requests.get((url.format(artifact_id)),
                                proxies={"http": "http://{}".format(proxy)})
        dependencies = set()
        soup = BeautifulSoup(response.text, 'lxml')
        div_ims = soup.find_all(class_='im')
        div_im = div_ims[0]
        detail_url = div_im.find(name='a')['href']
        group_id = detail_url.split('/')[2]
        response = requests.get(('https://mvnrepository.com{}'.format(detail_url)),
                                proxies={"http": "http://{}".format(proxy)})
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all(class_='versions')[0]
        trs = table.select('tr')[1:]
        trs = sorted(trs, key=lambda tr: int(tr.find(class_='rb').find_previous_sibling().string), reverse=True)
        dependencies = set(map(lambda tr: Dependence(artifact_id, group_id, tr.find(class_='vbtn').string), trs))
        return dependencies

    def nexus(self, proxy, url, **kwargs):
        artifact_id = kwargs['artifact_id']
        accurate = kwargs['accurate']
        response = requests.post(url,
                                 data='{"action": "coreui_Search", "method": "read", "type": "rpc", "tid": 1, "data": [{"page": 1,"start":0,"limit":300,"filter":[{"property":"keyword","value":"%s"}]}]}' % artifact_id,
                                 headers={'Content-Type': 'application/json'},
                                 proxies={'http': 'http://{}'.format(proxy)})
        dependencies = set()
        if accurate:
            dependencies = set(map(lambda item: Dependence(item['name'], item['group'], item['version']),
                                   filter(lambda item: item['a'] == artifact_id,
                                          json.loads(response.text)['result']['data'])))
        else:
            dependencies = set(map(lambda item: Dependence(item['name'], item['group'], item['version']),
                                   json.loads(response.text)['result']['data']))

        return dependencies
