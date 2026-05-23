from pydantic import BaseModel,ConfigDict,Field

##setting fileds for contraints
class PostBase(BaseModel):
    title:str=Field(min_length=1,max_length=100)
    content:str=Field(min_length=1)
    author:str=Field(min_length=1,max_length=50)

class PostCreate(PostBase):
    pass

##adding default data genrated by system
class PostResponse(PostBase):
    model_config=ConfigDict(from_attribute=True) ##enables the data to be read from database where it is not in dict format

    id:int
    date_posted: str