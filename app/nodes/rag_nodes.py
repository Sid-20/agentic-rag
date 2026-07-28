from app.nodes.parent_node import Node
from app.state.rag_state import RagState
from langchain_classic.document_loaders import PyPDFLoader,PDFPlumberLoader,UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import uuid
from app.client.langchain_llm import LLM_Chain
from app.prompts.base_prompts import chat_prompt
from langchain_core.messages import AIMessage
from langsmith import traceable


class RAG_Node(Node):

    def __init__(self, llm_client:LLM_Chain ,openai_key:str , chunk_size=450, chunk_overlap=50):
        self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        self.embeddings=OpenAIEmbeddings(api_key=openai_key,model='text-embedding-3-small')
        self.llm_client=llm_client
        self.vector_store=None
        self.loader=None
        self.retriever=None

    @traceable(name="load_docs",tags=["PyPDFLoader","Document Loader"])
    def load_document(self, state : RagState):
        file_path=state['file_path']
        self.loader=UnstructuredPDFLoader(file_path=file_path)
        docs=self.loader.load()

        print(f"----DOCUMENT LOADED----")

        return {'all_docs':docs}


    @traceable(name="create_chunks",tags=["Recursive Text Splitter","Chunk Creation"])
    def create_chunks(self, state : RagState):
        all_docs=state['all_docs']
        chunks=self.text_splitter.split_documents(all_docs)
        
        ids=[]
        for chunk in chunks:
            chunk.id=str(uuid.uuid4())
            ids.append(chunk.id)
        
        print(f"----CHUNKS CREATED----")
        
        return {'all_chunks':chunks , 'ids':ids}
        

    @traceable(name="storage_of_chunks",tags=["Chroma DB","VectorDB","OpenAI Embeddings"])
    def create_and_store_embeddings(self,state:RagState):

        chunks=state['all_chunks']
        ids=state['ids']

        adds=self.vector_store.add_documents(documents=chunks,ids=ids)

        print(f"----CHUNKS EMBEDDED INTO VECTOR DB----")


    def retrieve_relevant_documents(self,state:RagState):

        query=state['current_query']
        relevant_docs=self.retriever.invoke(query)

        print(f"----RELEVANT DOCS RETRIEVED----")

        return {'relevant_docs':relevant_docs}


    @traceable(name="check_collection_exists",tags=["start of the flow"])
    def check_condition_if_embeddings_exist(self,state:RagState):

        collection_name=state['collection_name']

        self.vector_store=Chroma(persist_directory='langgraph_rag',collection_name=collection_name,
                                 embedding_function=self.embeddings)
        
        self.retriever=self.vector_store.as_retriever(search_type='mmr',search_kwargs={'k':7,'fetch_k':20,'lamda_mult':0.7})
        
        print(f"----CHECKING CONDITION ----")
        
        if self.vector_store._collection.count()>0:

            print(f"----COLLECTION ALREADY EXISTS----")
            return True

        else:
            print(f"----COLLECTION TO BE CREATED----")
            return False
    

    def get_llm_response(self,state:RagState):

        print(f"-----GENERATRING LLM RESPONSE-----")

        query=state['current_query']
        relevant_docs=state['relevant_docs']
        history= [message.content for message in state['messages'] ]
        values={'query':query,'relevant_docs':relevant_docs,'chat_history':history}

        latest_message=self.llm_client.get_llm_chain_response(prompt=chat_prompt,values=values)

        print(f"AI response : {latest_message.response}")

        return {'messages':[AIMessage(content=latest_message.response)]}
   
    


    def get_all_nodes(self):
        pass



