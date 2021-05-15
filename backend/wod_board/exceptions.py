from fastapi import status
from fastapi.exceptions import HTTPException


class WodBoardException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super(Exception, self).__init__(f"{self.message}: {detail}")


class DuplicatedEmail(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Email already used"


class DuplicatedMovement(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "movement already used"


class DuplicatedRoundPosition(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Rounds have the same position"


class DuplicatedUsername(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Username already used"


class NameAlreadyUsed(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Name already used"


class TitleAlreadyUsed(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Title already used"


class UnknownEquipment(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This equipment doesn't exist"


class UnknownGoal(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This goal doesn't exist"


class UnknownMovement(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This movement doesn't exist"


class UnknownRound(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This round doesn't exist"


class UnknownUnit(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This unit doesn't exist"


class UnknownUser(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This user doesn't exist"


class UnknownWodType(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This type doesn't exist"


class UnknownWod(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "This WOD doesn't exist"


class UserIsNotAuthor(WodBoardException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Author don't match with authenticated user"


class UserIsNotAdmin(WodBoardException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Need admin rights"


class InvalidToken(WodBoardException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Could not validate credentials"


class RouterException(HTTPException):
    def __init__(self, error: WodBoardException) -> None:
        super().__init__(status_code=error.status_code, detail=error.message)
