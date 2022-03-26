from myapp.application.domain.model.karma import Karma


def test_karma_created_with_value():
    karma = Karma(10)
    assert karma.value == 10


def test_karma_equals():
    assert Karma(10) == Karma(10)


def test_karma_not_equals():
    assert Karma(10) != Karma(20)
