from flask import jsonify

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

unauthroized_response = MessageResponse(
    message='Unauthorized access'
)

def notFoundResponse(object=None, value=None):
    if object is None:
        object = 'Object'
     return MessageResponse(
        message='%s is not found' % object,
        body=value
     )
