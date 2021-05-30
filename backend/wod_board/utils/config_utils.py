import os
import typing

from wod_board import exceptions


def get_env_or_raise(env_name: str) -> str:
    value: typing.Optional[str] = os.getenv(env_name)

    if value is None:
        raise exceptions.MissingEnvVar(env_name)

    return value
