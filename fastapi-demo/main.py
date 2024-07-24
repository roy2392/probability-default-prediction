from fastapi import FastAPI
app = FastAPI()
#api = FastAPI()
#my_first_api = FastAPI()
#@my_first_api.get("/")
@app.get("/") # path operation decorator
async def root():
    return {"message":"Hello World from FASTAPI"}

@app.get("/demo") # path operation decorator
def demo_func():
    return {"message":" THis output from demo function "}
@app.post("/post_demo") # path operation decorator
def demo_post():
    return {"message":" This output from post demo function "}
# POST : to create DATA
# GET: to read DATA
# PUT: to update data
# DELETE:to delete data
# @app.post
# @app.delete
# @app.put