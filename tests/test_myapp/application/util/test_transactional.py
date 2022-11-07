from myapp.application.util.transactional import transactional


def test_does_not_decorate_when_testing(settings):
    settings.TESTING = True

    def dummy(): pass
    transactional_dummy = transactional(dummy)

    assert dummy is transactional_dummy


def test_decorates_when_running_production(settings):
    settings.TESTING = False

    def dummy(): pass
    transactional_dummy = transactional(dummy)

    assert dummy is not transactional_dummy
