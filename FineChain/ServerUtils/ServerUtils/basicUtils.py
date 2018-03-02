from flask import jsonify

unauthroized_response = MessageResponse(
    message='Unauthorized access',
).toJson()

class MessageResponse:
    message = 'Failure'
    body = '{}'

    def __init__(self, message, body):
        self.message = message
        self.body = body

    def toJson(self):
        return jsonify(
            message=self.message,
            body=self.body
        )
