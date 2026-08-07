
from langchain_core.prompts import PromptTemplate
from app.schema.response import llm_parser

def get_joke_prompt():

    prompt=PromptTemplate.from_template("""
    
    Given the topic {topic} , you're job is to generate a one liner joke on it.
    Have a look at the previous failed versions if present : {previous_versions}.
    The Latest Joke has to be funny than those. Try your best to achieve the results.
    \n.
    {format_instructions}

    """,
    partial_variables={'format_instructions':llm_parser.get_format_instructions()})

    return prompt