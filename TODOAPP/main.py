from fastapi import FastAPI


from .database import engine, Base
from .routers import auth, todo, admin, user

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def check_health():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)
