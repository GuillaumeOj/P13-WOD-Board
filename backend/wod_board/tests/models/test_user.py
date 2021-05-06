import pytest
import sqlalchemy.exc

from wod_board.models import user


def test_user(db):
    new_user = user.User(
        email="foo@bar.com",
        password="foo-password",
        username="foo-username",
        first_name="foo",
        last_name="bar",
        is_admin=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    assert str(new_user) == f"<User {new_user.email}>"

    new_user = user.User(
        password="foo-password",
        username="foo-username",
        is_admin=False,
    )
    db.add(new_user)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()
    db.rollback()
    assert (
        'null value in column "email" of relation "user" '
        "violates not-null constraint" in str(error)
    )

    new_user = user.User(
        email="foo@bar.com",
        username="foo-username",
        is_admin=False,
    )
    db.add(new_user)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()
    db.rollback()
    assert (
        'null value in column "password" of relation "user" '
        "violates not-null constraint" in str(error)
    )

    new_user = user.User(
        email="foo@bar.com",
        password="foo-password",
        is_admin=False,
    )
    db.add(new_user)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()
    db.rollback()
    assert (
        'null value in column "username" of relation "user" '
        "violates not-null constraint" in str(error)
    )

    new_user = user.User(
        email="foo@bar.com",
        password="foo-password",
        username="foo-username",
    )
    db.add(new_user)
    with pytest.raises(sqlalchemy.exc.IntegrityError) as error:
        db.commit()
    db.rollback()
    assert (
        'null value in column "is_admin" of relation "user" '
        "violates not-null constraint" in str(error)
    )
