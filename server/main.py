from fastapi import FastAPI, HTTPException
from validation_models import ValidUser, ValidTodo, ValidUserChanges, ValidTodoChanges
from api_functions import create_user, create_todo, get_user_info, get_todo_info, get_todo_by_tag, get_todo_by_user, update_user, update_todo, delete_user, delete_todo
from exceptions import InvalidEmail, NameAlreadyExists, UserNotFound, TodoNotFound
from database import db_dependency

app = FastAPI(debug=True)


@app.post("/api/v1/user")
async def api_create_user(user: ValidUser, db: db_dependency):
    try:
        await create_user(user, db)
    except InvalidEmail as e:
        raise HTTPException(400, detail=f"invalid Email: {user.mail}")
    except NameAlreadyExists as e:
        raise HTTPException(400, detail=f"name already exist: {user.name}")
    except Exception as e:
        raise HTTPException(500)
    

@app.post("/api/v1/todo")
async def api_create_todo(todo: ValidTodo, db: db_dependency):
    try:
        await create_todo(todo, db)
    except UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)


@app.get("/api/v1/user/")
async def api_user_info(user_id: int, db: db_dependency):
    try:
        result = await get_user_info(user_id, db)
    except UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo/")
async def api_todo_info(todo_id: int, db: db_dependency):
    try:
        result = await get_todo_info(todo_id, db)
    except TodoNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo_by_tag/")
async def api_todo_by_tag(tag: str, db: db_dependency):
    try:
        result = await get_todo_by_tag(tag, db)
    except TodoNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo_by_user/")
async def api_todo_by_user(user_id: int, db: db_dependency):
    try:
        result = await get_todo_by_user(user_id, db)
    except TodoNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)
    return result


@app.put("/api/v1/user/")
async def api_update_user(user_changes: ValidUserChanges, db: db_dependency):
    try:
        await update_user(user_changes, db)
    except InvalidEmail as e:
        raise HTTPException(400, detail=f"invalid Email: {user_changes.mail}")
    except NameAlreadyExists as e:
        raise HTTPException(400, detail=f"name already exist: {user_changes.name}")
    except UserNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)


@app.put("/api/v1/todo/")
async def api_update_todo(todo_changes: ValidTodoChanges, db: db_dependency):
    try:
        await update_todo(todo_changes, db)
    except TodoNotFound as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)
    

@app.delete("/api/v1/user/")
async def api_delete_user(user_id: int, db: db_dependency):
    try:
        await delete_user(user_id, db)
    except UserNotFound as e:
        HTTPException(404, "User not found")
    except Exception as e:
        raise HTTPException(500)


@app.delete("/api/v1/todo/")
async def api_delete_todo(todo_id: int, db: db_dependency):
    # import ipdb; ipdb.set_trace()
    try:
        await delete_todo(todo_id, db)
    except TodoNotFound as e:
        HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500)



# @app.get("/api/v1/todo_by_creator/")
# async def api_todo_by_creator(creator_id: int, db: db_dependency):
#     try:
#         result = await get_todo_by_creator(creator_id, db)
#     except TodoNotFound as e:
#         raise HTTPException(404, str(e))
#     except Exception as e:
#         raise HTTPException(500)
#     return result


# @app.get("/api/v1/user_by_todo/")
# async def api_user_by_todo(todo_id: int, db: db_dependency):
#     try:
#         result = await get_user_by_todo(user_id, db)
#     except UserNotFound as e:
#         raise HTTPException(404, str(e))
#     except Exception as e:
#         raise HTTPException(500)
#     return result


@app.post("/api/v1/tea")
async def teapot():
    raise HTTPException(418)