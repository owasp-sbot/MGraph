from unittest                                   import TestCase
from mgraph_db.providers.llms.utils.API__LLM    import API__LLM, ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import load_dotenv, get_env, env_value
from osbot_utils.utils.Objects                  import obj


class test_API__LLM(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        if not get_env(ENV_NAME_OPEN_AI__API_KEY):
            import pytest
            pytest.skip(f"{ENV_NAME_OPEN_AI__API_KEY} not set")

        cls.api_llm = API__LLM()

    def test_execute(self):
        system_prompt = 'today is monday the 13 of December 2025, just reply with the exact answer'
        user_prompt   = "what is today's month?"
        payload       = { "model": "gpt-4o-mini",
                          "messages": [{"role": "system", "content": system_prompt} ,
                                       {"role": "user"  , "content": user_prompt} ] }
        response       = self.api_llm.execute(payload)
        assert obj(response).choices[0].message.content == 'December'