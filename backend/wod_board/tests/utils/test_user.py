import pytest

from wod_board.models import user
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


def test_create_access_token():
    data = user.User(email="foo@bar.com")
    token = user_utils.create_access_token(data)

    assert isinstance(token, user_schemas.Token)


def test_get_current_user(db, db_user):
    token = user_utils.create_access_token(db_user)
    expected_user = user_utils.get_user_with_token(db, token.access_token)
    assert expected_user.id == db_user.id

    with pytest.raises(user_utils.InvalidToken):
        user_utils.get_user_with_token(db, "foo-token")

    token = user_utils.create_access_token(user.User(email="foo@emaill.com"))
    with pytest.raises(user_utils.InvalidToken):
        user_utils.get_user_with_token(db, token.access_token)
