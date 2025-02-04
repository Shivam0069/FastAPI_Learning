# FastAPI Project

This is a FastAPI project. Below are the details of the routes created in this project.

## Routes

### GET /

- **Description**: Root endpoint, returns a welcome message.
- **Response**: `{"message": "Welcome to FastAPI"}`

### GET /items/{item_id}

- **Description**: Retrieve an item by its ID.
- **Parameters**:
  - `item_id` (path): The ID of the item to retrieve.
- **Response**: `{"item_id": item_id, "name": "Item Name"}`

### POST /items/

- **Description**: Create a new item.
- **Request Body**:
  - `name` (string): The name of the item.
- **Response**: `{"item_id": new_item_id, "name": "Item Name"}`

### PUT /items/{item_id}

- **Description**: Update an existing item by its ID.
- **Parameters**:
  - `item_id` (path): The ID of the item to update.
- **Request Body**:
  - `name` (string): The new name of the item.
- **Response**: `{"item_id": item_id, "name": "Updated Item Name"}`

### DELETE /items/{item_id}

- **Description**: Delete an item by its ID.
- **Parameters**:
  - `item_id` (path): The ID of the item to delete.
- **Response**: `{"message": "Item deleted successfully"}`

## Running the Project

To run the project, use the following command:

```bash
uvicorn main:app --reload
```

This will start the FastAPI server and you can access the API documentation at `http://127.0.0.1:8000/docs`.
