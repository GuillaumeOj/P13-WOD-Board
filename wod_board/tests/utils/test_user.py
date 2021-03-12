from wod_board.models import user as user_models
from wod_board.schemas import user as user_schemas
from wod_board.utils import user as user_utils


def test_create_access_token():
    data = user_models.User(email="foo@bar.com")

    token = user_utils.create_access_token(data)

    assert isinstance(token, user_schemas.Token)


def test_get_user_with_token(db):
    user = user_models.User(
        email="foo@bar.com", username="foo_bar", hashed_password="hashed-password"
    )

    db.add(user)
    db.commit()

    token = user_utils.create_access_token(user)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert isinstance(user_with_token, user_models.User)
    assert user_with_token.email == user.email
    assert user_with_token.username == user.username

    user_2 = user_models.User(
        email=None, username="foo_bar", hashed_password="hashed-password"
    )
    token = user_utils.create_access_token(user_2)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert user_with_token is None

    user_3 = user_models.User(
        email="foo2@bar.com", username="foo_bar", hashed_password="hashed-password"
    )
    token = user_utils.create_access_token(user_3)

    user_with_token = user_utils.get_user_with_token(db, token)
    assert user_with_token is None


def test_authenticate_user(db):
    password = "strong-password"
    hashed_password = user_utils.PASSWORD_CTXT.hash(password)
    user = user_models.User(
        email="foo@bar.com", username="foo", hashed_password=hashed_password
    )

    db.add(user)
    db.commit()

    authentication = user_utils.authenticate_user(db, user.email, password)
    assert authentication.email == user.email

    authentication = user_utils.authenticate_user(db, "foo2@bar2.com", password)
    assert authentication is None

    authentication = user_utils.authenticate_user(db, user.email, "wrong-password")
    assert authentication is None
