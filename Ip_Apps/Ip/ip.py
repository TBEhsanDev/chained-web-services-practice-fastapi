import json

import uvicorn as uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post('/')
async def ip(request: Request):
    client_ip = request.headers.get('X-Real-IP')
    body=await request.body()
    if body:
        body = await request.json()
    else:
        body = dict()
    if client_ip:
        body['client_ip'] = client_ip
    return  body


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)
