"""
Tests for deocde_config module
"""
from decode_config import decode_config


def test_decode_config():
    """
    Tests config file can be decoded and tests it can be decoded if file is edited
    """
    assert decode_config()
    assert decode_config('empty.json') == ("Exeter", "ltla", "England", "", "", 'covid_image.jpeg')
