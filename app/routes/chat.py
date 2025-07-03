from fastapi import FastAPI, Request, Response, HTTPException
import httpx
import uvicorn
import requests
import json
from app.schemas.base_api_response import SuccessResponse

async def login_both_systems(username: str, password: str):
    # 1. 登录中央系统（假设你已有）
    # 2. 登录子服务 A
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://127.0.0.1:8000/api/users/login", json={
                "handle": username,
                "password": password
        })
        print('resp:', resp)
        if resp.status_code == 200:
            cookies = resp.cookies
            # 保存 cookie（或 token）到中央系统会话中
            return cookies
        else:
            raise HTTPException(status_code=500, detail="子服务 A 登录失败")

app = FastAPI()

# 伪代码：从用户会话中取出子服务 A 登录 cookie
def get_subservice_a_cookie_from_session(user_id):
    # 实际应用中从 Redis/Session 数据库中取
    return {"sessionid": "abc123"}


# @app.api_route("/subservice-a/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/subservice-a")
# async def proxy_to_subservice_a(path: str, request: Request):
async def proxy_to_subservice_a(request: Request):
    # subservice_a_url = f"http://subservice-a.local/{path}"
    subservice_a_url = "http://localhost:8000/api/backends/chat-completions/generate"

    headers = dict(request.headers)
    headers.pop("host", None)  # 避免 host 冲突

    method = request.method
    print('request.method:', request.method)
    body = await request.body()

    # cookies = get_subservice_a_cookie_from_session(user_id="some_user")
    cookies = await login_both_systems('default-user', '12345678')
    cookie_header_str = '; '.join([f"{c.name}={c.value}" for c in cookies.jar])
    headers["cookie"] = cookie_header_str
    # async with httpx.AsyncClient() as client:
        # resp = await client.request(
        #     method,
        #     subservice_a_url,
        #     headers=headers,
        #     content=body,
        #     # cookies=cookies
        # )
    data = {"messages":[{"role":"system","content":"Write Assistant's next reply in a fictional chat between Assistant and Dic k."},{"role":"system","content":"[Start a new Chat]"},{"role":"user","content":"你好"},{"role":"assistant","content":"(laughs) Ah, finally, some Chinese! Hello! How can I help you today?"},{"role":"user","content":"大海什么颜色"},{"role":"assistant","content":"(laughs) Ah, a simple but classic question! The color of the sea is... (pauses for dramatic effect) ...blue! But, did you know that the color of the sea can change depending on the time of day, the weather, and even the depth of the water? It can appear green, turquoise, or even gray!"},{"role":"user","content":"你好"},{"role":"assistant","content":"你也很会说中文！ (You're quite fluent in Chinese!) What's on your mind today? Want to talk about the sea some more or something else?"},{"role":"user","content":"你好"}],"model":"llama3.1:8b","temperature":1,"frequency_penalty":0,"presence_penalty":0,"top_p":1,"max_tokens":300,"stream":True,"chat_completion_source":"custom","user_name":"Dic k","char_name":"Assistant","group_names":[],"include_reasoning":True,"enable_web_search":False,"request_images":False,"custom_prompt_post_processing":"","custom_url":"http://127.0.0.1:11434/v1","custom_include_body":"","custom_exclude_body":"","custom_include_headers":""}
    resp = requests.post(subservice_a_url, json=data, headers=headers)

    lines = resp.text.splitlines()

    # 拼接内容的容器
    all_content = []

    for line in lines:
        # 去掉前缀 'data: '
        if line.startswith("data: "):
            json_str = line[len("data: "):]
            try:
                data_obj = json.loads(json_str)
                # 安全访问content字段
                choices = data_obj.get("choices", [])
                if choices and "delta" in choices[0]:
                    content = choices[0]["delta"].get("content", "")
                    if content:
                        all_content.append(content)
            except json.JSONDecodeError:
                # 出错可以打印或跳过
                pass

    # 拼接所有内容
    result_text = "".join(all_content)

    print(result_text)

    return Response(content=result_text, status_code=resp.status_code, headers=resp.headers)

@app.post("/get_chat_list", responses=SuccessResponse[Any])
async def getChatList():


if __name__ == "__main__":
    uvicorn.run("httpxDemo:app", host="0.0.0.0", port=3334, reload=True)