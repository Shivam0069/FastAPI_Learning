from ..routers.todo import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        completed=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "completed": False,
            "title": "Learn to code!",
            "description": "Need to learn everyday!",
            "id": 1,
            "priority": 5,
            "owner_id": 1,
        }
    ]


def test_read_one(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "completed": False,
        "title": "Learn to code!",
        "description": "Need to learn everyday!",
        "id": 1,
        "priority": 5,
        "owner_id": 1,
    }


def test_read_one_not_found():
    response = client.get("/todos/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "completed": False,
    }

    response = client.post("/todos", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.completed == request_data.get("completed")


def test_update_todo(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "completed": False,
    }

    response = client.put("/todos/1", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change the title of the todo already saved!"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "completed": False,
    }

    response = client.put("/todos/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todos/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
