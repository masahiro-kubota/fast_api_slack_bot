#function_app.py

import logging

import azure.functions as func 
from fastapi import FastAPI, Request, Response
from slack_bolt.adapter.fastapi import SlackRequestHandler

from routers import hello, slack_api

logging.basicConfig(level=logging.INFO)

api = FastAPI() 
api.include_router(hello.router)
api.include_router(slack_api.router)

@api.get("/")
async def root():
    logging.warning("Root")
    return {"message":"Hello world"}

@api.get("/error")
async def error():
    logging.warning("Error")
    print("This is print statement")
    raise ValueError("This is an error")


app = func.AsgiFunctionApp(app=api, http_auth_level=func.AuthLevel.ANONYMOUS)