import threading

import redis
import requests
import uvicorn
from fastapi import FastAPI, Request, HTTPException, status

app = FastAPI()
req_num = 100
lock = threading.Lock()
r = redis.Redis()


@app.post('/')
async def rate_limit(request: Request):
    client_ip = request.headers.get('X-Real-IP')
    ip = str(client_ip)
    lock.acquire()
    if not r.exists(ip):
        r.set(ip, req_num)
    print(r.get(ip))
    if r.get(ip) == b'0':
        lock.release()
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    r.decrby(ip, 1)
    lock.release()
    headers = request.headers
    body = await request.body()
    if body:
        body = await request.json()
    else:
        body = dict()
    try:
        resp = requests.post(url='http://127.0.0.1:6000/', json=body, headers=headers)
        return resp.json()
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


if __name__ == '__main__':
    uvicorn.run("__main__:app", host='127.0.0.1', port=5000, reload=True)
