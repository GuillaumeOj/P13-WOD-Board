from wod_board.schemas import user_schemas


def test_user_create():
    password = "very-strong-password"
    new_user_schema = user_schemas.UserCreate(
        email="foo@bar.com", username="foo", password=password
    )
    assert new_user_schema.password != password
