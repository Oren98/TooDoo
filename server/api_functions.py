from database import db_dependency
from validation_models import ValidUser, ValidTodo, ValidUserChanges, ValidTodoChanges
from database_models import Users, Todos, UserTodoRelations
from email_validator import validate_email, EmailNotValidError
from exceptions import InvalidEmail, UsersDatabaseError, TodosDatabaseError, UserTodoRelationsDatabaseError, NameAlreadyExists, UserNotFound, TodoNotFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from consts import RESULT_PER_QUERY


async def email_validator(email: str):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        raise InvalidEmail(str(e))


async def create_user(user: ValidUser, db: db_dependency):
    await email_validator(user.mail)
    db_user = Users(
        name= user.name,
        password= user.password,
        mail= user.mail)
    try:
        db.add(db_user)
        db.commit()
    except IntegrityError as e:
        raise NameAlreadyExists(str(e))
    except Exception as e:
        raise UsersDatabaseError(str(e))


async def create_todo(todo: ValidTodo, db: db_dependency):
    # add to todo table
    db_todo = Todos(
        title= todo.title,
        description= todo.description,
        priority= todo.priority,
        deadline= todo.deadline,
        reminder= todo.reminder,
        tags= todo.tags,
        creator= todo.creator
    )
    try:
        db.add(db_todo)
        db.flush()
        db.refresh(db_todo)
    except IntegrityError as e:
        raise UserNotFound(f"creator not found: {todo.creator}")
    except Exception as e:
        raise TodosDatabaseError(str(e))
    
    
    # add to user_todo_relations table
    db_relations = UserTodoRelations(
        user_id=db_todo.creator,
        todo_id=db_todo.id
    )
    try:
        db.add(db_relations)
        db.commit()
    except Exception as e:
        raise UserTodoRelationsDatabaseError(str(e))


async def is_empty(result, exception: Exception, err_msg: str):
    if (result is None):
        raise exception(err_msg)
    if (type(result) is list) and not result:
        raise exception(err_msg)
    return result


async def get_user_info(user_id: int, db: db_dependency):
    result = db.get(Users, user_id)
    return await is_empty(result, UserNotFound, "user not found")


async def get_todo_info(todo_id: int, db: db_dependency):
    result = db.get(Todos, todo_id)
    return await is_empty(result, TodoNotFound, "todo not found")


async def get_todo_by_tag(tag: str, db: db_dependency):
    statemant = db.execute(select(Todos).where(Todos.tags.contains(f'{{{tag}}}'))).fetchmany(RESULT_PER_QUERY)
    result = [todo_tuple[0] for todo_tuple in statemant]
    return await is_empty(result, TodoNotFound, "todo not found")


async def get_todo_by_user(user_id: int, db: db_dependency):
    statemant = db.execute(select(Todos).join(UserTodoRelations).where(UserTodoRelations.user_id == user_id)).fetchmany(RESULT_PER_QUERY)
    result = [todo_tuple[0] for todo_tuple in statemant]
    return await is_empty(result, TodoNotFound, "todo not found")


async def clean_changes(raw_changes: dict) -> dict:
    changes = {}
    for key, value in raw_changes.items():
        if (value is not None) and (key != 'id'):
            changes[key] = value
    return changes


async def update_user(user_changes: ValidUserChanges, db: db_dependency):
    user_changes_clean = await clean_changes(user_changes.model_dump())
    email = user_changes_clean.get('mail')
    if email is not None:
        await email_validator(email)
    
    statemant = update(Users).where(Users.id == user_changes.id).values(user_changes_clean)
    try:
        result = db.execute(statemant)
        db.commit()
    except IntegrityError as e:
        raise NameAlreadyExists()
    except Exception as e:
        raise UsersDatabaseError(str(e))
    if result.rowcount == 0:
        raise UserNotFound()
    if result.rowcount < 0:
        raise UsersDatabaseError(str(e))


async def update_todo(todo_changes: ValidTodoChanges, db: db_dependency):
    todo_changes_clean = await clean_changes(todo_changes.model_dump())
    statemant = update(Todos).where(Todos.id == todo_changes.id).values(todo_changes_clean)
    try:
        result = db.execute(statemant)
        db.commit()
    except Exception as e:
        raise TodosDatabaseError(str(e))
    if result.rowcount == 0:
        raise TodoNotFound("Todo not found")
    if result.rowcount < 0:
        raise TodosDatabaseError(str(e))


async def delete_relations_by_user(user_id: int, db: db_dependency):
    statement = delete(UserTodoRelations).where(UserTodoRelations.user_id == user_id)
    try:
        db.execute(statement)
        db.flush()
    except Exception as e:
        raise UsersDatabaseError
    

async def delete_todo_by_user(user_id: int, db: db_dependency):
    statement = delete(Todos).where(Todos.creator == user_id)
    try:
        db.execute(statement)
        db.flush()
    except Exception as e:
        raise UsersDatabaseError
    

async def delete_from_users(user_id: int, db: db_dependency):
    statement = delete(Users).where(Users.id == user_id)
    try:
        result = db.execute(statement)
        db.commit()
    except Exception as e:
        raise UsersDatabaseError
    if result.rowcount == 0:
        raise UserNotFound("User not found")
    if result.rowcount < 0:
        raise UsersDatabaseError(str(e))


async def delete_user(user_id: int, db: db_dependency):
    await delete_relations_by_user(user_id, db)
    await delete_todo_by_user(user_id, db)
    await delete_from_users(user_id, db)


async def delete_relations_by_todo(todo_id: int, db: db_dependency):
    statement = delete(UserTodoRelations).where(UserTodoRelations.todo_id == todo_id)
    try:
        result = db.execute(statement)
        db.flush()
    except Exception as e:
        raise TodosDatabaseError()
    if result.rowcount == 0:
        raise TodoNotFound("Todo not found")
    if result.rowcount < 0:
        raise TodosDatabaseError(str(e))


async def delete_from_todos(todo_id: int, db: db_dependency):
    statement = delete(Todos).where(Todos.id == todo_id)
    try:
        result = db.execute(statement)
        db.commit()
    except Exception as e:
        raise TodosDatabaseError()
    if result.rowcount == 0:
        raise TodoNotFound("Todo not found")
    if result.rowcount < 0:
        raise TodosDatabaseError(str(e))


async def delete_todo(todo_id: int, db: db_dependency):
    await delete_relations_by_todo(todo_id, db)
    await delete_from_todos(todo_id, db)
    
# async def get_todo_by_creator(user_id: int, db: db_dependency):
#     result = db.query(Todos).filter(Todos.creator == user_id).limit(RESULT_PER_QUERY).all()
#     return await is_empty(result, TodoNotFound, "todo not found")
