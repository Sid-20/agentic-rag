from fastapi import FastAPI

from app.routes.potter_chat import potterchat_router

app=FastAPI()

#app.include_router(chat_router)
app.include_router(potterchat_router)

