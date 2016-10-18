class Response:
    def __init__(self, content, private=False, file=False):
        self.content = content
        self.private = private
        self.file = file