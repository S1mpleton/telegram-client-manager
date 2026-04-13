from pydantic import BaseModel, Field



class ClientLaunchSchema(BaseModel):
    client_name: str = Field(max_length=16)



