from langgraph.graph import StateGraph,START,END
from app.state.job_state import JobState
from app.nodes.job_nodes import Job_Node
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from app.db.database import connection_obj
from langchain_core.messages import HumanMessage

class JobBot:

    def __init__(self, nodes : Job_Node):
        self.graph=StateGraph(JobState)
        self.nodes= nodes
        self.create_workflow()
    

    def create_workflow(self):

        self.graph.add_node('chat_node',self.nodes.chat_node)
        self.graph.add_node('tools',self.nodes.tool_node)

        self.graph.add_edge(START,'chat_node')
        self.graph.add_conditional_edges('chat_node',tools_condition)
        self.graph.add_edge('tools','chat_node')
        self.graph.add_edge('chat_node',END)

        checkpointer=SqliteSaver(conn=connection_obj)

        self.workflow=self.graph.compile(checkpointer=checkpointer)


    
    def get_graph_overview(self):

        if self.workflow:
            graph = self.workflow.get_graph()

            png = graph.draw_mermaid_png()
            return{'content':'CREATED','overview':png}
      
        return {'content':'Yet to create WORKFLOW'}
    



    def ask_query(self,query:str,username:str):

        config={"configurable":{'thread_id':username}}
        initial_state={'messages':[HumanMessage(content=query)],'current_query':query}

        final_state=self.workflow.invoke(initial_state,config=config)
        return final_state


    def get_chat_history(self,username:str):

        config={"configurable":{'thread_id':username}}

        return self.workflow.get_state(config=config).values["messages"]
