class TypeFilter:
    def __init__(self):
        self.type_name:str

    def from_string(self, value:str):
        return value

    def to_string(self, value) -> str:
        pass

    def check(self, value:str) -> bool:
        if value:
            return True
        return True

class TypeFilterString(TypeFilter):
    def __init__(self):
        super().__init__()
        self.type_name = "String"

    def from_string(self, value:str) -> str:
        return value

    def to_string(self, value:str) -> str:
        return str(value)

    def check(self, value:str) -> bool:
        return True

class TypeFilterBoolean(TypeFilter):
    def __init__(self):
        super().__init__()
        self.type_name = "Boolean"

    def from_string(self, value:str) -> bool:
        match value:
            case "true":
                return True
            case "false":
                return False
        return None

    def to_string(self, value:bool) -> str:
        return str(value)

    def check(self, value:str) -> bool:
        if value in ["true", "false"]:
            return True
        return False

class TypeFilterInt(TypeFilter):
    def __init__(self):
        super().__init__()
        self.type_name = "Integer"

    def from_string(self, value:str) -> int:
        return int(value)

    def to_string(self, value:int) -> str:
        return str(value)

    def check(self, value:str) -> bool:
        try:
            int(value)
        except Exception:
            return False
        return True

class Filters:
    STRING = TypeFilterString()
    INT = TypeFilterInt()
    BOOL = TypeFilterBoolean()

filters = Filters()