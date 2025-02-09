from fastapi import FastAPI, Request
from .database import engine, Base
from .routers import auth, todo, admin, user
from fastapi.templating import Jinja2Templates

app = FastAPI()

Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="TODOAPP/templates")


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/healthy")
def check_health():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
