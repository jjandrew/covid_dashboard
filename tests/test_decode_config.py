import json
from decode_config import decode_config


def test_decode_config_exists():
    assert decode_config()


def test_decode_config_deals_with_key_errors():
    assert decode_config('empty.json') == ("", "", "", "", "", 'covid_image.jpeg')
