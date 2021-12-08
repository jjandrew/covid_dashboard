"""Tests for the time_conversions module to be run using Pytest
"""
from time_conversions import time_difference


def test_time_difference():
    """Tests invalid entries to time_difference function return None
    """
    assert time_difference("2324") is None
    assert time_difference("abc:12") is None
    assert time_difference("12:a") is None
    assert time_difference("25:10") is None
    assert time_difference("10:62") is None
    assert time_difference("-01:20") is None
    assert time_difference("02:-10") is None
