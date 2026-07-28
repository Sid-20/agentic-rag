from langgraph.graph import StateGraph,START,END
from app.state.rag_state import RagState
from app.nodes.rag_nodes import RAG_Node
from langgraph.checkpoint.sqlite import SqliteSaver
from app.db.database import connection_obj
from langchain_core.messages import HumanMessage

class PotterBot:

    def __init__(self, nodes : RAG_Node):
        self.graph=StateGraph(RagState)
        self.nodes=nodes

    def create_workflow(self):

        self.graph.add_node('load_docs',self.nodes.load_document)
        self.graph.add_node('create_chunks',self.nodes.create_chunks)
        self.graph.add_node('embed_and_store_chunks',self.nodes.create_and_store_embeddings)
        self.graph.add_node('retrieve_relevant_docs',self.nodes.retrieve_relevant_documents)
        self.graph.add_node('get_llm_response',self.nodes.get_llm_response)


        self.graph.add_conditional_edges(START,self.nodes.check_condition_if_embeddings_exist,
                                         {True:'retrieve_relevant_docs',False:'load_docs'})
        
        self.graph.add_edge('load_docs','create_chunks')
        self.graph.add_edge('create_chunks','embed_and_store_chunks')
        self.graph.add_edge('embed_and_store_chunks','retrieve_relevant_docs')
        self.graph.add_edge('retrieve_relevant_docs','get_llm_response')
        self.graph.add_edge('get_llm_response',END)

        checkpointer=SqliteSaver(conn=connection_obj)

        self.workflow=self.graph.compile(checkpointer=checkpointer)
    

    def get_graph_overview(self):

        if self.workflow:
            graph = self.workflow.get_graph()

            png = graph.draw_mermaid_png()
            return{'content':'CREATED','overview':png}
      
        return {'content':'Yet to create WORKFLOW'}
    


    def get_chat_history(self,thread_id):

        config={"configurable":{"thread_id":thread_id}}

        return self.workflow.get_state(config=config).values["messages"]

    

    def ask_query(self,query,file_path,collection_name,user_name):

        config={'configurable':{'thread_id':user_name}}

        initial_state={'messages':[HumanMessage(content=query)],'file_path':file_path,
                       'current_query':query,'collection_name':collection_name}
        
        final_state=self.workflow.invoke(initial_state,config=config)
        return final_state


