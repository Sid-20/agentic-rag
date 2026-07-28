from fastapi.routing import APIRouter
from fastapi import Depends
from app.core.dependencies import get_potterbot_client
from fastapi import Response,HTTPException

from pathlib import Path

potterchat_router=APIRouter(prefix='/potter',tags=['HarryPotter'])


@potterchat_router.get('/create_workflow')
def create_workflow(chatbot_client=Depends(get_potterbot_client)):

    chatbot_client.create_workflow()
    return Response(content='WORKFLOW CREATED')



@potterchat_router.get("/get_overview")
def get_graph_overview(chatbot_client=Depends(get_potterbot_client)):

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


@potterchat_router.post("/chat")
def chat(query:str,file_name:str,user_name:str,chatbot_client=Depends(get_potterbot_client)):

    
    BASE_DIR = Path(__file__).resolve().parents[3]
    DATA_DIR = BASE_DIR / "data"

    file_path = DATA_DIR / file_name

    collection_name=file_name.split('.')[0]
    response=chatbot_client.ask_query(query,file_path,collection_name,user_name)

    content=[r.content for r in response["messages"]]

    return {'AI RESPONSE':content[-1]}


@potterchat_router.get("/get_history")
def get_history(user_name:str,chatbot_client=Depends(get_potterbot_client)):

    history=chatbot_client.get_chat_history(user_name)

    messages=[h.content for h in history]

    return messages