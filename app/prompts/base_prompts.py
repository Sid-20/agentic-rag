

from langchain_core.prompts import ChatPromptTemplate
from app.schema.response import llm_parser


chat_prompt=ChatPromptTemplate.from_template("""

Based on the user query {query} and the context :\n {relevant_docs}  , generate an appropriate response. \n
Here is the chat_history as well : {chat_history}
\n
{format_instructions}. H
""",
partial_variables={'format_instructions':llm_parser.get_format_instructions()})