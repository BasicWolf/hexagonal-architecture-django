from myapp.application.domain.model.karma import Karma
from myapp.application.domain.model.specification.specification import Specification


class KarmaEnoughForVotingSpecification(Specification):
    MINIMUM_KARMA_REQUIRED_FOR_VOTING = Karma(5)

    def is_satisfied_by(self, karma: Karma) -> bool:
        return karma.value >= self.MINIMUM_KARMA_REQUIRED_FOR_VOTING.value
