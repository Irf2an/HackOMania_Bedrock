from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

# Initialize OpenAI models
llm1 = ChatOpenAI(model_name="gpt-4", temperature=0.3)
llm2 = ChatOpenAI(model_name="gpt-4", temperature=0.3)

