class InvalidConfigError(Exception):
    def __init__(self, message):
        self.message = f'Parsing of config failed: {message.lower()}'
        super().__init__(self.message)


class ApiHttpError(Exception):
    def __init__(self, message, code=500):
        self.code = code
        self.message = f'Request to server failed: {message.lower()}'
        super().__init__(self.message)

