from langgraph.graph import StateGraph,START,END
from app.nodes.joke_node import Joke_Node
from app.state.joke_state import JokeState
from langgraph.checkpoint.sqlite import SqliteSaver
from app.db.database import connection_obj
from langgraph.types import Command

class Joke_bot:

    def __init__(self,node:Joke_Node):
        self.nodes=node
        self.graph=StateGraph(JokeState)
        self.create_workflow()
        

    def create_workflow(self):

        self.graph.add_node('generate_joke',self.nodes.generate_joke)
        self.graph.add_node('approve_joke',self.nodes.approve_joke)

        self.graph.add_edge(START,'generate_joke')
        self.graph.add_edge('generate_joke','approve_joke')
        self.graph.add_conditional_edges('approve_joke',self.nodes.check_condition,{'yes':END,'no':'generate_joke'})

        checkpointer=SqliteSaver(conn=connection_obj)

        self.workflow=self.graph.compile(checkpointer=checkpointer)


    def tell_joke(self,topic,username,approval=None):

        config={"configurable":{'thread_id':username}}
        if approval:
            final_state=self.workflow.invoke(Command(resume={"approval":approval}),config=config)
            return final_state

        
        initial_state={'topic':topic,'previous_versions':[]}

        final_state=self.workflow.invoke(initial_state,config=config)
        return final_state




    def get_graph_overview(self):
    
            if self.workflow:
                graph = self.workflow.get_graph()
    
                png = graph.draw_mermaid_png()
                return{'content':'CREATED','overview':png}
          
            return {'content':'Yet to create WORKFLOW'}



