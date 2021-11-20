from myapp.application.domain.model.karma import Karma


def test_karma_created_with_value():
    karma = Karma(10)
    assert karma.value == 10


def test_karma_is_enough_for_voting():
    karma = Karma(10)
    assert karma.enough_for_voting()


def test_karma_is_not_enough_for_voting():
    karma = Karma(4)
    assert not karma.enough_for_voting()


def test_karma_equals():
    assert Karma(10) == Karma(10)


def test_karma_not_equals():
    assert Karma(10) != Karma(20)
