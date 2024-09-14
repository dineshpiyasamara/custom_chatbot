from langchain_community.llms import HuggingFaceHub
import os
from dotenv import load_dotenv
from params import *
from langchain_openai import ChatOpenAI

load_dotenv()

def huggingface_llm():
      llm = HuggingFaceHub(
            repo_id = LLM_REPO_ID,
            model_kwargs = {"temperature":TEMPERATURE, "max_length":MAX_LENGTH},
            huggingfacehub_api_token = os.getenv('HUGGINGFACE_API_KEY')
            )
      return llm

def openai_llm():
      os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

      llm = ChatOpenAI(
      model="gpt-3.5-turbo",
      temperature=0
      )
      return llm