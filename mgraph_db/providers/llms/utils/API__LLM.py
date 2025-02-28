from typing                             import Dict, Any
from osbot_utils.type_safe.Type_Safe    import Type_Safe
from osbot_utils.utils.Env              import get_env
from osbot_utils.utils.Http             import POST_json
from osbot_utils.utils.Json             import json_parse

DEFAULT__LLM__SELECTED_PLATFORM = "OpenAI (Paid)"
DEFAULT__LLM__SELECTED_PROVIDER = "OpenAI"
DEFAULT__LLM__SELECTED_MODEL    = "gpt-4o"

ENV_NAME_OPEN_AI__API_KEY = "OPEN_AI__API_KEY"

class API__LLM(Type_Safe):
    api_url     : str = "https://api.openai.com/v1/chat/completions"
    api_key_name: str = ENV_NAME_OPEN_AI__API_KEY

    def execute(self, llm_payload : Dict[str, Any]):
        url = self.api_url

        headers = { "Authorization": f"Bearer {self.api_key()}",
                    "Content-Type" : "application/json"       ,
                    'User-Agent'   : "myfeeds.ai"             }
        response = POST_json(url, headers=headers, data=llm_payload)                #todo: add error handling
        return response

    # todo: refactor this into a separate class with better error detection and context specific methods
    def get_json(self, llm_response):
        choices  = llm_response.get('choices')
        if len(choices) == 1:
            message = choices[0].get('message')
            if 'function_call' in message:
                arguments = message.get('function_call').get('arguments')
            else:
                arguments = message.get('tool_calls')[0].get('function').get('arguments')
        else:
            return choices
        return json_parse(arguments)


    def get_json__entities(self, llm_response):
        function_arguments = self.get_json(llm_response)
        return function_arguments.get('entities')

    def api_key(self):
        api_key = get_env(self.api_key_name)
        if not api_key:
            raise ValueError("{self.api_key_name} key not set")
        return api_key