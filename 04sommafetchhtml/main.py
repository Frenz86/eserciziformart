from fastapi import FastAPI,status,Depends
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="API-Somma", description="with FastAPI by Daniele Grotti", version="1.0")

class Numbers(BaseModel):
    num1: float =5
    num2: float =6

from fastapi.middleware.cors import CORSMiddleware
# Allow CORS (Cross-Origin Resource Sharing) for javascipt response
"""Is a mechanism that allows restricted resources on a web page to be requested 
from another domain outside the domain from which the first resource was served. """
app.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )

######################################################################

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {" ---->          http://localhost:8000/docs     <----------"}


#@app.get("/sum/{num1}/{num2}")
@app.get("/sum")
async def get_sumnumbers(numbers: Numbers= Depends()):
    try:
        res = numbers.num1 + numbers.num2
        return {"result": res}
    except:
        return {"result": "error"}

@app.post("/sum")
async def post_sumnumbers(numbers: Numbers):
    try:
        res = numbers.num1 + numbers.num2
        return {"result": res}
    except:
        return {"result": "error"}

#######################################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

