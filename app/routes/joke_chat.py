from fastapi.routing import APIRouter
from app.core.dependencies import get_joke_client
from fastapi import Response,HTTPException,Depends
from typing import Literal,Optional

joke_router=APIRouter(prefix="/joke",tags=['Jokes'])


@joke_router.post("/ask")
def ask_query(query:str,username:str,approval:Optional[Literal['yes','no']] | None=None,joke_client=Depends(get_joke_client)):

    if approval:
        response=joke_client.tell_joke(topic=query,username=username,approval=approval)
    else:
        response=joke_client.tell_joke(topic=query,username=username)

    return response

    # latest_message=response['messages'][-1]

    # return {"AI": response['current']}





@joke_router.get("/get_overview")
def get_graph_overview(joke_client=Depends(get_joke_client)):

    try:
        response= joke_client.get_graph_overview()

        if response.get('content')=='CREATED':
            return Response(
                    content=response.get('overview'),
                    media_type="image/png"
                )
        
        return Response(content='NO WORKFLOW CREATED')
    
    except Exception as e:

        return HTTPException(status_code=501,detail=f"Exception {e}")
