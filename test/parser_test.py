import unittest
from parser import Parser
from proxy_tool import get_proxy


class ParserTest(unittest.TestCase):
    def test_parse_mvncentral(self):
        parser = Parser()
        dependencies = parser.mvn_central(proxy=get_proxy(), artifact_id='poi')
        assert len(dependencies) > 0
