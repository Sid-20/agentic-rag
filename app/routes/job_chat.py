from fastapi.routing import APIRouter
from fastapi import Depends

from fastapi import Response,HTTPException
from app.core.dependencies import get_job_client
from app.schema.response import llm_parser



job_router=APIRouter(prefix='/job',tags=['Job'])


@job_router.get("/get_overview")
def get_graph_overview(chatbot_client=Depends(get_job_client)):

    try:
        response= chatbot_client.get_graph_overview()

        if response.get('content')=='CREATED':
            return Response(
                    content=response.get('overview'),
                    media_type="image/png"
                )
        
        return Response(content='NO WORKFLOW CREATED')
    
    except Exception as e:

        return HTTPException(status_code=501,detail=f"Exception {e}")


@job_router.post("/ask")
def ask_query(query:str,username:str,job_client=Depends(get_job_client)):

    response=job_client.ask_query(query=query,username=username)

    latest_message=response['messages'][-1]

    return {"AI": latest_message.content}


@job_router.get("/get_chat_history")
def get_history(username:str,job_client=Depends(get_job_client)):

    response=job_client.get_chat_history(username=username)

    messages=[message.content for message in response]
   
    return messages