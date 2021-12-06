import json
from decode_config import decode_config


def test_decode_config_exists():
    assert decode_config()
    assert decode_config('empty.json') == ("Exeter", "ltla", "England", "", "", 'covid_image.jpeg')
