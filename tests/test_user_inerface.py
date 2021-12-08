"""Unit Tests for the user_interface part of the application to be run using Pytest
"""
from user_interface import event_update
from user_interface import event_exists
from user_interface import add_update


def test_event_update():
    """Tests events can be updated and are returned in the correct format
    """
    events = event_update("test event", "test content", "both", False, True)
    assert events == [{'title': "test event", 'content': "test content",
                       'to_update': "both", 'repeat': False}]


def test_event_exists():
    """Tests it is possible to check whether an event is present in scheduled events
    """
    assert event_exists("test event1", True) is False
    assert event_exists('test event', True) is True


def test_add_update():
    """Tests that is is not possible to add updates with invalid entries
    """
    assert add_update(False, True, True, 'test event', "24:61") is False
    assert add_update(False, False, False, 'test event', "21:51") is False
