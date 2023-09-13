class InvalidEmail(Exception):
    pass


class UsersDatabaseError(Exception):
    pass


class NameAlreadyExists(Exception):
    pass


class TodosDatabaseError(Exception):
    pass


class UserTodoRelationsDatabaseError(Exception):
    pass


class UserNotFound(Exception):
    pass


class TodoNotFound(Exception):
    pass


class DBSetupFailure(Exception):
    pass
