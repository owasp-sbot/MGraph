#import requests
from typing                              import Dict, Any
from osbot_utils.type_safe.Type_Safe    import Type_Safe
from osbot_utils.utils.Env              import get_env
from osbot_utils.utils.Json             import json_parse

DEFAULT__LLM__SELECTED_PLATFORM = "OpenAI (Paid)"
DEFAULT__LLM__SELECTED_PROVIDER = "OpenAI"
DEFAULT__LLM__SELECTED_MODEL    = "gpt-4o"

ENV_NAME_OPEN_AI__API_KEY = "OPEN_AI__API_KEY"

class API__LLM(Type_Safe):


    def execute(self, llm_payload : Dict[str, Any]):
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key()}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=llm_payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    # todo: refactor this into a separate class with better error detection and context specific methods
    def get_json(self, llm_response):
        choices  = llm_response.get('choices')
        if len(choices) == 1:
            message = choices[0].get('message').get('function_call').get('arguments')
        else:
            return choices
        return json_parse(message)


    def get_json__entities(self, llm_response):
        function_arguments = self.get_json(llm_response)
        return function_arguments.get('entities')

    def api_key(self):
        api_key = get_env(ENV_NAME_OPEN_AI__API_KEY)
        if not api_key:
            raise ValueError("{ENV_NAME_OPEN_AI__API_KEY} key not set")
        return api_key

    # todo: add
    # def execute(self, system_prompts:list, user_prompt: str):
    #
    #     with self.llm_execution_simple as _:
    #         kwargs = dict( llm_platform   = DEFAULT__LLM__SELECTED_PLATFORM,
    #                        llm_provider   = DEFAULT__LLM__SELECTED_PROVIDER,
    #                        llm_model      = DEFAULT__LLM__SELECTED_MODEL   ,
    #                        system_prompts = system_prompts,
    #                        user_prompt    = user_prompt,
    #                        stream         = False)
    #
    #         result           = _.execute(**kwargs)
    #         return result
    #
    # def get_json(self, result):
    #     return result
