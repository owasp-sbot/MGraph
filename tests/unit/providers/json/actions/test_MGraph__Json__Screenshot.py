import pytest
from unittest                                                       import TestCase
from mgraph_ai.providers.json.MGraph__Json                          import MGraph__Json
from mgraph_ai.providers.json.actions.MGraph__Json__Export          import MGraph__Json__Export
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph    import Domain__MGraph__Json__Graph
from osbot_utils.utils.Files                                        import file_delete
from osbot_utils.utils.Env                                          import load_dotenv
from mgraph_ai.providers.json.actions.MGraph__Json__Screenshot      import MGraph__Json__Screenshot


class test_MGraph__Json__Screenshot(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.test_data = {"aa": "bb", "cc": ["dd", "ee"], "an_list": [1, 2, 3, 4]}
        cls.target_file     = '/tmp/json-screenshot.png'
        cls.delete_on_exit  = False
        cls.mgraph_json     = MGraph__Json()
        cls.json_screenshot = cls.mgraph_json.screenshot()
        if cls.json_screenshot.url__render_server() is None:
            pytest.skip("No URL for rendering MGraph__Json__Screenshot")
        cls.mgraph_json.load().from_data(cls.test_data)

    @classmethod
    def tearDownClass(cls):
        if cls.delete_on_exit:
            assert file_delete(cls.target_file) is True

    def test__setUpClass(self):
        with self.json_screenshot as _:
            assert type(_      )  is MGraph__Json__Screenshot
            assert type(_.graph) is Domain__MGraph__Json__Graph
            assert _.graph == self.mgraph_json.graph

    def test_export(self):
        with self.json_screenshot.export() as _:
            assert type(_) is MGraph__Json__Export

    def test_dot(self):
        result = self.json_screenshot.dot()
        assert result.startswith(b'\x89PNG\r\n\x1a\n') is True

    def test_mermaid(self):
        result = self.json_screenshot.mermaid()
        assert result.startswith(b'\x89PNG\r\n\x1a\n') is True
