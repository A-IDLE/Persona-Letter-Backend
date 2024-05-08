from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.runnables import ConfigurableField
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.outputs import LLMResult
from dotenv import load_dotenv

class StreamCallback(BaseCallbackHandler):
        def on_llm_new_token(self, token:str, **kwargs):
            print(token, end="", flush=True)

        def on_llm_end(self, response: LLMResult, **kwargs: any) -> any:
            """Run when LLM ends running."""


def load_model():
    
    load_dotenv()
    
    llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0,
            streaming=True,
            max_tokens= 500,   # 모델의 max_token 설정
            callbacks=[StreamCallback()],
        ).configurable_alternatives(
            # 이 필드에 id를 부여합니다
            # 최종 실행 가능한 객체를 구성할 때, 이 id를 사용하여 이 필드를 구성할 수 있습니다.
            ConfigurableField(id="llm"),
            # 기본 키를 설정합니다.
            default_key="gpt4",
            claude=ChatAnthropic(
                model="claude-3-opus-20240229",
                temperature=0,
                streaming=True,
                callbacks=[StreamCallback()],
            ),
            gpt3=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                streaming=True,
                callbacks=[StreamCallback()],
            ),
            ollama=ChatOllama(
                model="EEVE-Korean-10.8B:long",
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            ),
        )
    
    return llm


def load_make_character_model():
    
    load_dotenv()
    
    llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0,
            streaming=True,
            max_tokens= 2000,   # 모델의 max_token 설정
            callbacks=[StreamCallback()],
        ).configurable_alternatives(
            # 이 필드에 id를 부여합니다
            # 최종 실행 가능한 객체를 구성할 때, 이 id를 사용하여 이 필드를 구성할 수 있습니다.
            ConfigurableField(id="llm"),
            # 기본 키를 설정합니다.
            default_key="gpt4",
            claude=ChatAnthropic(
                model="claude-3-opus-20240229",
                temperature=0,
                streaming=True,
                callbacks=[StreamCallback()],
            ),
            gpt3=ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0,
                streaming=True,
                callbacks=[StreamCallback()],
            ),
            ollama=ChatOllama(
                model="EEVE-Korean-10.8B:long",
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            ),
        )
    
    return llm