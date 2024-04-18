from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)
import sys
from model import Todo
from fastapi import FastAPI, HTTPException
# Cross Origin Resourse Sharing acts as the bridge of networking btwn. frontend and backend. Ex, protocols
from fastapi.middleware.cors import CORSMiddleware

# App object
app = FastAPI()


origins = [
    "http://localhost:3000",  # Add the frontend origin here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Backend for Todo List Manager"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(
        404, f"There is no TODO item item with the title {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(
        400, "Something went wrong / Bad request")


@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(
        404, f"There is no TODO item item with the title {title}")


@app.delete("/api/todo{title}")
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo item!"
    raise HTTPException(
        404, f"There is no TODO item item with the title {title}")


# # Define the signal handler function
# def graceful_shutdown(signum, frame):
#     # Perform cleanup tasks here (e.g., closing database connections, saving state, etc.)
#     # ...

#     # Exit the application
#     sys.exit(0)


# # Register the signal handler for SIGTERM
# signal.signal(signal.SIGTERM, graceful_shutdown)

# # Your FastAPI routes and logic here
# # ...

# if __name__ == "__main__":
#     # Start the FastAPI application using uvicorn
#     uvicorn.run("app:app", host='0.0.0.0', port=8000,
#                 reload=True, debug=True, workers=3)
