
from app.config.settings import Settings

from functools import lru_cache
from app.client.langchain_llm import LLM_Chain
from app.schema.response import llm_parser
from app.nodes.rag_nodes import RAG_Node
from app.nodes.job_nodes import Job_Node
from app.workflow.rag_workflow import PotterBot
from app.workflow.job_workflow import JobBot



@lru_cache
def get_settings():
    settings=Settings()
    return settings

@lru_cache
def get_llm_chain_client():
    settings=get_settings()
    return LLM_Chain(openai_key=settings.OPENAI_KEY ,parser=llm_parser,openai_model=settings.OPENAI_MODEL)

@lru_cache
def get_job_nodes():
    return Job_Node(llm_client=get_llm_chain_client())

@lru_cache
def get_job_client():
    return JobBot(nodes=get_job_nodes())


@lru_cache
def get_rag_nodes_client():
    settings=Settings()
    return RAG_Node(openai_key=settings.OPENAI_KEY ,llm_client=get_llm_chain_client())

@lru_cache
def get_potterbot_client():
    return PotterBot(nodes=get_rag_nodes_client())


