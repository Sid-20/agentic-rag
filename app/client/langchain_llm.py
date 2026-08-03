from langchain_openai import ChatOpenAI
from app.schema.response import PydanticOutputParser


class LLM_Chain:

    def __init__(self , openai_key:str, parser : PydanticOutputParser , openai_model :  str):
        self.llm = ChatOpenAI(api_key=openai_key,model=openai_model)
        self.parser = parser
    
    def bind_tools(self,tools:list):
        self.llm=self.llm.bind_tools(tools)

    def get_llm_chain_response(self, prompt : str ,values : dict):
        chain = prompt | self.llm #| self.parser 
        return chain.invoke(values)
