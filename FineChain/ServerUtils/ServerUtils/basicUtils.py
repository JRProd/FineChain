from flask import jsonify

# Basic message response
class MessageResponse:
    message = 'Failure'
    body = None

    def __init__(self, message, body=None):
        self.message = message
        self.body = body

    def toJson(self):
        return jsonify(
            message=self.message,
            body=self.body
        )

# Predefined message
unauthroized_response = MessageResponse(
    message='Unauthorized access'
)

# Predefinced message
expired_token = MessageResponse(
    message='Your token has expired'
)

# Quick 404 response
def notFoundResponse(object=None, value=None):
    if object is None:
        object = 'Object'
    return MessageResponse(
        message='%s is not found' % object,
        body=value
     )
