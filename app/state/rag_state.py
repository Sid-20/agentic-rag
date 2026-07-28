from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.documents import Document


class RagState(TypedDict):

    messages : Annotated[list[BaseMessage],add_messages]
    relevant_docs : list[Document] 
    current_query : str
    collection_name :  str
    file_path : str
    all_docs : list[Document]
    all_chunks : list[Document]
    ids : list[str]