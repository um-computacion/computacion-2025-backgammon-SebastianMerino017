import random

def get_dice():
    try:
        dice_0 = random.randint(1, 6)
        dice_1 = random.randint(1, 6)
        return (dice_0, dice_1, dice_0, dice_1) if dice_0 == dice_1 else (dice_0, dice_1)
    except Exception:
        return ()

class Dice:
    def __init__(self):
        self.__values__ = []
        self.__used_values__ = []
    
    def roll(self):
        dice_result = get_dice()
        if len(dice_result) == 0:
            self.__values__ = []
            return ()
        self.__values__ = list(dice_result)
        self.__used_values__ = []
        return (dice_result[0], dice_result[1])
    
    def get_values(self):
        return self.__values__[:]
    
    def get_available_values(self):
        available = self.__values__[:]
        for used_value in self.__used_values__:
            if used_value in available:
                available.remove(used_value)
        return available
    
    def use_value(self, value):
        if value in self.get_available_values():
            self.__used_values__.append(value)
            return True
        return False
    
    def is_double(self):
        return len(self.__values__) == 4
    
    def has_available_values(self):
        return len(self.get_available_values()) > 0
    
    def __str__(self):
        if not self.__values__:
            return "Dados sin tirar"
        available = self.get_available_values()
        used = len(self.__used_values__)
        return (
            f"Tirada doble: {self.__values__[0]}, Disponibles: {len(available)}, Usados: {used}"
            if self.is_double()
            else f"Tirada: [{self.__values__[0]}, {self.__values__[1]}], Disponibles: {len(available)}, Usados: {used}"
        )
