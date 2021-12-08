"""Tests for decode_config module to run using Pytest
"""
from decode_config import decode_config


def test_decode_config():
    """Tests config file can be decoded

    Tests it can be decoded if file has been edited incorrectly
    """
    assert decode_config()
    assert decode_config('empty.json') == ("Exeter", "ltla", "England", "", "", 'covid_image.jpeg')
