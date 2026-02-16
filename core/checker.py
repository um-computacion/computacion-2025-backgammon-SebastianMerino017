class Checker:
    def __init__(self, color: str, position: int = None):
        self.__color__ = color
        self.__position__ = position
        self.__is_captured__ = False

    def get_color(self) -> str:
        return self.__color__

    def get_position(self) -> int:
        return self.__position__

    def set_position(self, position: int) -> None:
        self.__position__ = position

    def is_captured(self) -> bool:
        return self.__is_captured__

    def capture(self) -> None:
        self.__is_captured__ = True
        self.__position__ = None

    def release(self, position: int) -> None:
        self.__is_captured__ = False
        self.__position__ = position

    def __str__(self) -> str:
        status = "captured" if self.__is_captured__ else f"at position {self.__position__}"
        return f"{self.__color__} checker {status}"
