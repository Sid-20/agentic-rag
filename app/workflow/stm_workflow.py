from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.state.stm_state import ShortTermState
from app.nodes.stm_node import STM_Node
from app.db.database import connection_obj
from langchain_core.messages import HumanMessage


class STM_Bot:

    def __init__(self,nodes:STM_Node):
        self.nodes=nodes
        self.workflow=None
        self.create_workflow()



    def create_workflow(self):

        self.graph=StateGraph(ShortTermState)

        self.graph.add_node('chat_node',self.nodes.chat_node)
        self.graph.add_node('summarize',self.nodes.summarize_messages)


        self.graph.add_edge(START,'chat_node')
        self.graph.add_conditional_edges('chat_node',self.nodes.check_condition,{True:'summarize',False:END})
        self.graph.add_edge('summarize','chat_node')

        checkpointer=SqliteSaver(conn=connection_obj)

        self.workflow=self.graph.compile(checkpointer=checkpointer)



    def get_graph_overview(self):
    
            if self.workflow:
                graph = self.workflow.get_graph()
    
                png = graph.draw_mermaid_png()
                return{'content':'CREATED','overview':png}
          
            return {'content':'Yet to create WORKFLOW'}


    def ask_query(self,query:str,username:str):

         config={'configurable':{'thread_id':username}}

         initial_state={'latest_messages':[HumanMessage(content=query)],'summary':""}

         final_state=self.workflow.invoke(initial_state,config=config)

         return final_state['latest_messages']

    


    def get_chat_history(self,username:str,attribute:str):
         
        config={'configurable':{'thread_id':username}}

        return self.workflow.get_state(config=config).values[attribute]

