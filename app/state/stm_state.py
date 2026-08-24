
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated,TypedDict



class ShortTermState(TypedDict):

    latest_messages:Annotated[list[BaseMessage],add_messages]
    summary:str


