from fastapi import FastAPI

from app.routes.job_chat import job_router
from app.routes.joke_chat import joke_router

app=FastAPI()

#app.include_router(chat_router)
app.include_router(joke_router)

