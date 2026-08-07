from typing import TypedDict,Literal
from pydantic import Field



class JokeState(TypedDict):

    topic : str
    current_joke : str
    previous_versions : list[str]
    approved : Literal['yes','no']
    final_joke:str

