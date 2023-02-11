class InvlidRollFormatException(Exception):
    """Raised when a user enters a roll in an invalid format"""

    def __init__(
        self,
        roll: str = "",
        message: str = "The roll input is in an invalid format. Please try again.\nInput: ",
        *args: object
    ) -> None:
        self.message = message + roll
        super().__init__(self.message, *args)


class TooManyDiceException(Exception):
    def __init__(
            self,
            message: str = "Too many dice rolls being generated. Don't want to slow down the application.",
            *args: object
    ) -> None:
        self.message = message
        super().__init__(self.message, *args)
