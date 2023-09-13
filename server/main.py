from fastapi import FastAPI, HTTPException

from api_functions import (
    create_todo,
    create_user,
    delete_todo,
    delete_user,
    get_todo_by_tag,
    get_todo_by_user,
    get_todo_info,
    get_user_info,
    update_todo,
    update_user,
)
from database import db_dependency
from exceptions import InvalidEmail, NameAlreadyExists, TodoNotFound, UserNotFound
from logger import logger
from validation_models import ValidTodo, ValidTodoChanges, ValidUser, ValidUserChanges

# from configuration import validate_config


app = FastAPI(debug=True)


@app.post("/api/v1/user")
async def api_create_user(user: ValidUser, db: db_dependency):
    """
    api endpoint for creating user

    :param user: ValidUser object to represent user
    :param db: db connection
    :raises HTTPException: error 400 for invalid email
    :raises HTTPException: error 400 for existing name
    :raises HTTPException: error 500 for other
    """
    try:
        await create_user(user, db)
    except InvalidEmail:
        logger.error(f"invalid Email: {user.mail}, raising 400")
        raise HTTPException(400, detail=f"invalid Email: {user.mail}")
    except NameAlreadyExists:
        logger.error(f"name already exist: {user.name} raising 400")
        raise HTTPException(400, detail=f"name already exist: {user.name}")
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.post("/api/v1/todo")
async def api_create_todo(todo: ValidTodo, db: db_dependency):
    """
    api endpoint for creating todo

    :param todo: ValidTodo object to represent todo
    :param db: db connection
    :raises HTTPException: error 404 for not found creator
    :raises HTTPException: error 500 for other
    """
    try:
        await create_todo(todo, db)
    except UserNotFound as e:
        logger.error(f"creator user not found, user id = {todo.creator}, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.get("/api/v1/user")
async def api_user_info(user_id: int, db: db_dependency):
    """
    api endpoint for geting user info

    :param user_id: user id number
    :param db: db connection
    :raises HTTPException: error 404 incase user not found
    :raises HTTPException: error 500 for other
    :return: user info from db
    """
    try:
        result = await get_user_info(user_id, db)
    except UserNotFound as e:
        logger.error(f"user not found, user id = {user_id}, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo")
async def api_todo_info(todo_id: int, db: db_dependency):
    """
    api endpoint for getting todo info

    :param todo_id: todo id number
    :param db: db connection
    :raises HTTPException: error 404 if todo not found
    :raises HTTPException: error 500 for other
    :return: todo info from db
    """
    try:
        result = await get_todo_info(todo_id, db)
    except TodoNotFound as e:
        logger.error(f"todo not found, todo id = {todo_id}, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo_by_tag")
async def api_todo_by_tag(tag: str, db: db_dependency):
    """
    api endpoint for getting todo's info by tag

    :param tag: tag to search for
    :param db: db connection
    :raises HTTPException: error 404 if todo not found
    :raises HTTPException: error 500 for other
    :return: info of the todos that are tagged with the given tag
    """
    try:
        result = await get_todo_by_tag(tag, db)
    except TodoNotFound as e:
        logger.error(f'no todo found with this tag, tag = "{tag}", raising 404')
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)
    return result


@app.get("/api/v1/todo_by_user")
async def api_todo_by_user(user_id: int, db: db_dependency):
    """
    api endpoint for getting todos by user

    :param user_id: user id number
    :param db: db connection
    :raises HTTPException: error 404 if user not found
    :raises HTTPException: error 500 for other
    :return: todos by the given user
    """
    try:
        result = await get_todo_by_user(user_id, db)
    except TodoNotFound as e:
        logger.error(
            f"not todo found that it is connected with this user, user id = {user_id}, raising 404"
        )
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)
    return result


@app.put("/api/v1/user")
async def api_update_user(user_changes: ValidUserChanges, db: db_dependency):
    """
    api endpoint to update user

    :param user_changes: user info to update
    :param db: db connection
    :raises HTTPException: error 404 if email is invalid
    :raises HTTPException: error 400 if name already exist
    :raises HTTPException: error 404 if user not found
    :raises HTTPException: error 500 for other
    """
    try:
        await update_user(user_changes, db)
    except InvalidEmail:
        logger.error(f"invalid Email: {user_changes.mail}")
        raise HTTPException(400, detail=f"invalid Email: {user_changes.mail}")
    except NameAlreadyExists:
        logger.error(f"name already exist: {user_changes.name} raising 400")
        raise HTTPException(400, detail=f"name already exist: {user_changes.name}")
    except UserNotFound as e:
        logger.error(f"user not found, user id = {user_changes.id}, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.put("/api/v1/todo")
async def api_update_todo(todo_changes: ValidTodoChanges, db: db_dependency):
    """
    api endpoint to update todo

    :param todo_changes: todo info to update
    :param db: db connection
    :raises HTTPException: error 404 if todo not found
    :raises HTTPException: error 500 for other
    """
    try:
        await update_todo(todo_changes, db)
    except TodoNotFound as e:
        logger.error(f"todo not found, todo id = {todo_changes.id}, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.delete("/api/v1/user")
async def api_delete_user(user_id: int, db: db_dependency):
    """
    api endpoint to delete user

    :param user_id: user id number
    :param db: db connection
    :raises HTTPException: error 404 if user not found
    :raises HTTPException: error 500 for other
    """
    try:
        await delete_user(user_id, db)
    except UserNotFound:
        logger.error(f"user not found, user id = {user_id}, raising 404")
        raise HTTPException(404, "User not found")
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.delete("/api/v1/todo")
async def api_delete_todo(todo_id: int, db: db_dependency):
    """
    api endpoint to delete todo

    :param todo_id: _description_
    :param db: _description_
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    """
    try:
        await delete_todo(todo_id, db)
    except TodoNotFound as e:
        logger.error("todo not found, raising 404")
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(500)


@app.post("/api/v1/tea")
async def teapot():
    """
    api endpoint for teapot

    :raises HTTPException: _description_
    """
    logger.info("I'm a Teapot")
    raise HTTPException(418, "I'm a Teapot")
