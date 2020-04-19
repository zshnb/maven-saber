import unittest
from parser import Parser
from proxy_tool import get_proxy


class ParserTest(unittest.TestCase):
    def test_parse_mvncentral(self):
        parser = Parser()
        dependencies = parser.mvn_central(proxy=get_proxy(), artifact_id='poi')
        assert len(dependencies) > 0

    def test_parse_nexus(self):
        parser = Parser()
        dependencies = parser.nexus('localhost:8081', 'http://localhost:8081/service/extdirect', artifact_id='spring', accurate=False)
        assert len(dependencies) >= 0
