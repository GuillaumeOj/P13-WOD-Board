from wod_board.utils import schemas_utils


def test_to_camel_case():
    assert schemas_utils.to_camel_case("test_to_camel_case") == "testToCamelCase"
