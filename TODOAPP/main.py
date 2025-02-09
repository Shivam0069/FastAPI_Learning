from .routers import auth, todo, admin, user
from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="TODOAPP/static"), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def check_health():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
