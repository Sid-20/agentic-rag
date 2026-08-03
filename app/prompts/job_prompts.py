from langchain_core.prompts import ChatPromptTemplate
from .base_prompts import llm_parser

def get_job_prompt():

    prompt=ChatPromptTemplate.from_template("""
    Given the user query {query} and the message history : {chat}, Answer the user. \n

    """)

    return prompt