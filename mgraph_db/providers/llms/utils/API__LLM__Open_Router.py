from mgraph_db.providers.llms.utils.API__LLM import API__LLM

ENV_NAME_OPEN_ROUTER__API_KEY = "OPEN_ROUTER__API_KEY"
OPEN_ROUTER__LLM_MODEL__GEMINI_2 = 'google/gemini-2.0-flash-lite-001'

class API__LLM__Open_Router(API__LLM):
    api_url     : str = "https://openrouter.ai/api/v1/chat/completions"
    api_key_name: str = ENV_NAME_OPEN_ROUTER__API_KEY