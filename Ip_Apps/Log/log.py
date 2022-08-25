import datetime
import json

import jsonlines
import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status

app = FastAPI()


def save_log(body):
    with jsonlines.open('log.jsonl', mode='a') as log:
        log.write(body)


@app.post('/')
async def log(request: Request):
    body = await request.body()
    if body:
        body = await request.json()
    else:
        body = dict()
    body['time'] = str(datetime.datetime.now())
    save_log(body)
    del body['time']
    headers = request.headers
    try:
        resp = requests.post('http://127.0.0.1:8000/', json=body, headers=headers)
        return resp.json()
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


if __name__ == '__main__':
    uvicorn.run("__main__:app", host='127.0.0.1', port=6000, reload=True)
