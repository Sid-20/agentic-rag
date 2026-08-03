from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class JobState(TypedDict):

    messages: Annotated[list[BaseMessage],add_messages]
    current_query : str
