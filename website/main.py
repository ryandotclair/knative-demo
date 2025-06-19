from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from redis import Redis
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Try to get the real client IP from X-Forwarded-For
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # The header can contain multiple IPs, the first is the real client
        real_ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Fallback to the direct client IP
        real_ip = request.client.host
    
    # Grab the redis's blacklist collection
    redis_client = Redis(host="redis.website.svc.cluster.local", port=6379)
    if redis_client.sismember("banned", real_ip):
        return templates.TemplateResponse("banned.html", {"request": request, "requestorIp": real_ip})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "requestorIp": real_ip})