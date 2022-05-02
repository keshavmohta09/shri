class RollbackException(Exception):
    """
    Exception used to rollback a transaction and send a message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
