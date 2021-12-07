from user_interface import event_update
from user_interface import event_exists
from user_interface import add_update


def test_event_update():
    events = event_update("test event", "test content", "both", False, True)
    assert events == [{'title': "test event", 'content': "test content",
                       'to_update': "both", 'repeat': False}]


def test_event_exists():
    assert event_exists("test event1", True) is False
    assert event_exists('test event', True) is True


def test_add_update():
    assert add_update(False, True, True, 'test event', "24:61") is False
    assert add_update(False, False, False, 'test event', "21:51") is False
