from wod_board.models import user
from wod_board.schemas import user_schemas
from wod_board.utils import user_utils


def test_create_access_token():
    data = user.User(email="foo@bar.com")

    token = user_utils.create_access_token(data)

    assert isinstance(token, user_schemas.Token)


def test_get_user_with_token(db):
    user_1 = user.User(
        email="foo@bar.com", username="foo_bar", hashed_password="hashed-password"
    )

    db.add(user_1)
    db.commit()

    token = user_utils.create_access_token(user_1)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert isinstance(user_with_token, user.User)
    assert user_with_token.email == user_1.email
    assert user_with_token.username == user_1.username

    user_2 = user.User(
        email=None, username="foo_bar", hashed_password="hashed-password"
    )
    token = user_utils.create_access_token(user_2)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert user_with_token is None

    user_3 = user.User(
        email="foo2@bar.com", username="foo_bar", hashed_password="hashed-password"
    )
    token = user_utils.create_access_token(user_3)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert user_with_token is None


def test_authenticate_user(db):
    password = "strong-password"
    hashed_password = user_utils.PASSWORD_CTXT.hash(password)
    user_1 = user.User(
        email="foo@bar.com", username="foo", hashed_password=hashed_password
    )

    db.add(user_1)
    db.commit()

    authentication = user_utils.authenticate_user(db, user_1.email, password)
    assert authentication.email == user_1.email

    authentication = user_utils.authenticate_user(db, "foo2@bar2.com", password)
    assert authentication is None

    authentication = user_utils.authenticate_user(db, user_1.email, "wrong-password")
    assert authentication is None
