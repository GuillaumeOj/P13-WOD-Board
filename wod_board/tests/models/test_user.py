from wod_board.models import user


def test_user(db):
    new_user = user.User(
        email="foo@bar.com",
        hashed_password="foo-password",
        username="foo-username",
        first_name="foo",
        last_name="bar",
    )

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    assert str(new_user) == f"<User {new_user.email}>"
