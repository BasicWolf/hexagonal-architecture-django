from http import HTTPStatus

from rest_framework.response import Response


def problem_response(title: str, detail: str, status: HTTPStatus) -> Response:
    problem_data = {
        'title': title,
        'detail': detail,
        'status': status.value
    }
    return Response(
        problem_data,
        status=status.value,
        content_type='application/problem+json'
    )
