from pydantic import BaseModel


class SimpleMessage(BaseModel):
    """Model to represent a simple message from the api"""
    message: str

    @classmethod
    def ok(cls):
        """Message to use with 200 if nothing else makes sense"""
        return cls(message="ok")

    @classmethod
    def bad_request(cls):
        """Message to use with 400"""
        return cls(message="bad request")

    @classmethod
    def unauthorized(cls):
        """Message to use with 401"""
        return cls(message="unauthorized")

    @classmethod
    def denied(cls):
        """Message to use with 403"""
        return cls(message="permission denied")

    @classmethod
    def not_found(cls):
        """Message to use with 404"""
        return cls(message="not found")

    @classmethod
    def conflict(cls):
        """Message to use with 409"""
        return cls(message="conflict")
