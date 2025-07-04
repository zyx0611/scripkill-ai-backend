from pydantic import BaseModel

class ChatlistRequest(BaseModel):
    avatar_url: str
    ch_name: str
    file_name: str

class ChatlistContentResponse(BaseModel):
    uuid: str