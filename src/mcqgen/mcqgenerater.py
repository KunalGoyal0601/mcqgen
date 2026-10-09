import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
#from src.mcqgenerater.utils import read_file.get_table_data

#import necessary langchain packages
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.chains import SequentialChain

#load envirement variable from the .env file
load_dotenv()

#Access the envirement variable just like os.environ
key = os.getenv('huggingfacehub_api_token')

# 1. Initialize the base endpoint
# You don't even need to specify the task or provider; it will auto-route!
llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct", 
    temperature=0.7,
    max_new_tokens=256,
    huggingfacehub_api_token=key
)

# 2. Wrap it in ChatHuggingFace
# This tells Hugging Face: "Use the conversational task"
chat_model = ChatHuggingFace(llm=llm_endpoint)


# 3. Use ChatPromptTemplate instead of PromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI that generates multiple-choice questions."),
    ("human", "{question}")
])

# 4. Chain and run using LCEL
chain = prompt | chat_model

response = chain.invoke({"question": "What is the capital of France?"})

# The response is an AIMessage object, so we print the .content
print(response.content)