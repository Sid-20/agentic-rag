from fastapi import FastAPI

from app.routes.job_chat import job_router

app=FastAPI()

#app.include_router(chat_router)
app.include_router(job_router)

