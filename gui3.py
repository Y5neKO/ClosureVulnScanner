import asyncio
import logging
from fastapi import FastAPI, Response

# 设置日志记录级别
logging.basicConfig(level=logging.INFO)

# 创建FastAPI应用程序
app = FastAPI()

# 用于存储日志消息的列表
log_messages = []


# SSE路由
@app.get("/events")
async def events(response: Response):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Connection"] = "keep-alive"

    while True:
        if log_messages:
            yield "data: " + log_messages.pop(0) + "\n\n"
        else:
            await asyncio.sleep(1)


# 添加日志处理器
logger = logging.getLogger("uvicorn")
logger.addHandler(logging.StreamHandler())


# 在每条日志消息上注册一个回调函数，将其添加到log_messages列表中
def log_to_sse(message):
    log_messages.append(message)


logger.addFilter(log_to_sse)


# 路由
@app.get("/")
async def read_root():
    return {"message": "Server-Sent Events server is running"}


# 运行UVicorn服务器
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
