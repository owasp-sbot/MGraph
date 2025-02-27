from mgraph_db.providers.llms.utils.API__LLM import API__LLM

ENV_NAME_GROQ__API_KEY    = "GROQ__API_KEY"
GROQ__LLM_MODEL__MIXTRAL = 'Mixtral-8x7b-32768'

class API__LLM__Groq(API__LLM):
    api_url     : str = "https://api.groq.com/openai/v1/chat/completions"
    api_key_name: str = ENV_NAME_GROQ__API_KEY