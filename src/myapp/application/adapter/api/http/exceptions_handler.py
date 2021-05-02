import logging
from http import HTTPStatus

from rest_framework.views import exception_handler

from myapp.application.adapter.api.http.problem_response import problem_response
from myapp.application.domain.model.exceptions.entity_not_found import EntityNotFound

logger = logging.getLogger(__name__)


def exceptions_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    logger.error("Unexpected error occurred: %s", exc)

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, EntityNotFound):
        return problem_response("Error", str(exc), HTTPStatus.BAD_REQUEST)

    logger.exception("Unhandled error: %s", exc, exc_info=True)
    return problem_response(
        "Unknown error",
        "Our deepest apologies, an unexpected error occurred "
        "and we are already working on it.",
        HTTPStatus.INTERNAL_SERVER_ERROR
    )
