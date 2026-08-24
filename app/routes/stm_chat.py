from fastapi.routing import APIRouter
from fastapi import Depends
from app.core.dependencies import get_stm_client
from app.workflow.stm_workflow import STM_Bot
from fastapi import Response,HTTPException

stm_router=APIRouter(prefix="/stm",tags=["Short Term Memory"])



@stm_router.get("/get_overview")
def get_graph_overview(stm_client:STM_Bot=Depends(get_stm_client)):

    try:
        response= stm_client.get_graph_overview()

        if response.get('content')=='CREATED':
            return Response(
                    content=response.get('overview'),
                    media_type="image/png"
                )
        
        return Response(content='NO WORKFLOW CREATED')
    
    except Exception as e:

        return HTTPException(status_code=501,detail=f"Exception {e}")





@stm_router.post("/chat")
def chat(query:str,user_name:str,stm_client:STM_Bot=Depends(get_stm_client)):

    response=stm_client.ask_query(query=query,username=user_name)

    messages=[r.content for r in response]
    latest=messages[-1]

    return {'AI':latest}

    #return Response(content=latest)



@stm_router.get("/get_chat_history")
def get_chat_history(attribute:str,username:str,stm_client:STM_Bot=Depends(get_stm_client)):

    response=stm_client.get_chat_history(username=username,attribute=attribute)

    if attribute=="summary":
        return {'Summary':response}

    messages=[r.content for r in response]

    return {'Messages':messages}

    #return Response(content=messages)


