class Kakaoerror(Exception):
    def __init__(self, message, status):
        self.message = message,
        self.status  = status