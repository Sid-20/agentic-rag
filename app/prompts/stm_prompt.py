from langchain_core.prompts import ChatPromptTemplate
from app.schema.response import llm_parser


def get_chat_prompt():

    prompt=ChatPromptTemplate.from_template(''' 
    You are given recent messages of a user {latest_messages} along with a summarized version
    of his older messages : {summary}. Make sure that you answer the user correctly.\n

    {format_instructions}

    ''',
    partial_variables={'format_instructions':llm_parser.get_format_instructions()}
    )

    return prompt


def get_summary_prompt():

    prompt=ChatPromptTemplate.from_template(''' 
    You are given messages of a user {messages} and an old summary {old_summary}.
    Make sure to generate a summarized version of it combining all the provided info.\n
    {format_instructions}

    ''',
    partial_variables={'format_instructions':llm_parser.get_format_instructions()}
    )

    return prompt
