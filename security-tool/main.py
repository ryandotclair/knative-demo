import requests
import json
import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
# from loguru import logger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
redisURL = os.getenv("REDIS_URL", "redis.website.svc.cluster.local")

app = FastAPI(
    title="Security Tools",
    version="1.0.1",
    description="Provides detailed information about an IP address, including Country, Region (State), timezone, ISP (aka asnOrganization),and estimated city."
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KEY = os.getenv("KEY")

class MyPayload(BaseModel):
    ip: str


@app.post("/ip-classifier")
async def IPClassifier(payload: MyPayload):
    IP = payload.ip
    logging.info(f"IP received: {IP}")
    # Classify the IP address
    url = f"https://free.freeipapi.com/api/json/{IP}"
    try:
        response = requests.get(url)
        data = response.json()
        logging.info(json.dumps(data, indent=4))
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# Ban Hammer
@app.post("/ban-hammer")
async def BanHammer(payload: MyPayload):
    IP = payload.ip
    logging.info(f"IP received: {IP}")
    # Ban the IP address
    try:
        redis_client = Redis(host=redisURL, port=6379)
        redis_client.sadd("banned", IP)
        return {"message": "IP banned successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


# Unban Hammer
@app.post("/unban-hammer")
async def UnbanHammer(payload: MyPayload):
    IP = payload.ip
    logging.info(f"IP received: {IP}")
    # Unban the IP address
    try:
        redis_client = Redis(host=redisURL, port=6379)
        redis_client.srem("banned", IP)
        return {"message": "IP unbanned successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# Get Blacklist
@app.get("/get-blocklist")
async def GetBlocklist():
    # Get the blacklist
    try:
        redis_client = Redis(host=redisURL, port=6379)
        banned = redis_client.smembers("banned")
        if banned:
            return {"banned": list(banned)}
        else:
            return {"banned": "Empty"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")