from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.specification.karma_enough_for_voting import (
    KarmaEnoughForVotingSpecification
)


def test_karma_enough_for_voting():
    assert KarmaEnoughForVotingSpecification().is_satisfied_by(Karma(10))


def test_karma_not_enough_for_voting():
    assert not KarmaEnoughForVotingSpecification().is_satisfied_by(Karma(4))
