from langchain_community.callbacks.manager import get_openai_callback

class OpenAICallback:

    def __call__(self, *args, **kwds):
        return get_openai_callback(*args, **kwds)