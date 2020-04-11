import requests
import json
from proxy_tool import get_proxy
from dependence import Dependence


class Parser(object):
    def __init__(self):
        self.url = 'https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByWords?_input_charset=utf-8' \
                   '&queryTerm={}&repoId={}'


    def parse(self, keyword, repo_id='all'):
        dependencies = set()
        proxy = get_proxy()['proxy']
        response = requests.get((self.url.format(keyword, repo_id)), proxies={"http": "http://{}".format(proxy)})
        if response.status_code == 200:
            results = json.loads(response.text)['object']
            for item in results:
                dependencies.add(Dependence(item['artifactId'], item['groupId'], item['version']))

            return dependencies



# if __name__ == '__main__':
#     retry_count = 5
#     proxy = get_proxy().get("proxy")
#     while retry_count > 0:
#         try:
#             response = requests.get('https://maven.aliyun.com/artifact/aliyunMaven/searchArtifactByWords?_input_charset=utf-8&queryTerm=fastjson&repoId=all', proxies={"http": "http://{}".format(proxy)})
#             if response.status_code != 200:
#                 retry_count -= 1
#             else:
#                 json_result = json.loads(response.text)['object']
#                 for item in json_result:
#                     if item['artifactId'] == 'fastjson':
#                         print(item)
#                 break
#             # 使用代理访问
#             # return html
#         except Exception as e:
#             print(e)
#             retry_count -= 1
#     # 出错5次, 删除代理池中代理
#     delete_proxy(proxy)
