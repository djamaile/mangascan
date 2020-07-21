from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API is working"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict:
    return {"item_id": item_id}
