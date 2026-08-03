from .parent_node import Node
from app.tools.job_tools import job_tools
from langgraph.prebuilt import ToolNode
from app.client.langchain_llm import LLM_Chain
from app.state.job_state import JobState
from app.prompts.job_prompts import get_job_prompt
from langchain_core.messages import AIMessage

class Job_Node(Node):

    def __init__(self,llm_client:LLM_Chain):
        self.llm_client=llm_client
        self.llm_client.bind_tools(tools=job_tools)
        self.tool_node=ToolNode(job_tools)
        

    def chat_node(self, state: JobState):

        current_query=state['current_query']
        chat=state['messages']

        values={'query':current_query,'chat':chat}

        response=self.llm_client.get_llm_chain_response(prompt=get_job_prompt(),values=values)

        return {'messages':[response]}


    
    def get_all_nodes(self):
        pass

