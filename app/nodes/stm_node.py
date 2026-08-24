from app.state.stm_state import ShortTermState
from app.client.langchain_llm import LLM_Chain
from app.prompts.stm_prompt import get_chat_prompt,get_summary_prompt
from app.schema.response import llm_parser
from langchain_core.messages import AIMessage,RemoveMessage

class STM_Node:

    def __init__(self,llm_client:LLM_Chain):
        self.llm_client=llm_client
        

    def chat_node(self,state:ShortTermState):

        latest_messages=state['latest_messages']
        summary=state['summary']

        values={'latest_messages':latest_messages,'summary':summary}

        print(f"---calling chat node----{values}")

        response=self.llm_client.get_llm_chain_response(prompt=get_chat_prompt(),values=values)

        return {'latest_messages':[AIMessage(content=response.response)]}



    def summarize_messages(self,state:ShortTermState):

        messages=state['latest_messages']
        old_summary=state['summary']

        values={'messages':messages,'old_summary':old_summary}

        print(f"---calling summary node----{values}")

        response=self.llm_client.get_llm_chain_response(prompt=get_summary_prompt(),values=values)

        messages_to_delete = state["latest_messages"][:-2]

        return {
            "summary": response.response,
            "latest_messages": [RemoveMessage(id=m.id) for m in messages_to_delete],
        }

  

    def check_condition(self,state:ShortTermState):

        if len(state['latest_messages'])>=8:
            return True
        return False
