from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder

from myapp.application.domain.model.identifier.identifier import Identifier


class ApplicationJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Identifier):
            return super().default(obj.id)
        return super().default(obj)


class ApplicationJSONRenderer(JSONRenderer):
    encoder_class = ApplicationJSONEncoder

