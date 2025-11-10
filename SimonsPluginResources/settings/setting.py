from .scopes import Scope, GlobalScope
from .type_filters import TypeFilter, filters

class Setting:
    def __init__(self,
                 topic: str,
                 setting_id: str,
                 category: str = None,
                 description: str = "",
                 scope: Scope = GlobalScope(),
                 type_filter: TypeFilter = filters.STRING,
                 important: bool = True,
                 default_value: str = "",
                 current_value = None,
                 ):
        self.category: str = category
        self.scope: Scope = scope
        self.topic: str = topic
        self.setting_id: str = setting_id
        self.description: str = description
        self.type_filter: TypeFilter = type_filter
        self.important: bool = important
        self.default_value: str = default_value
        self.current_value_str: str = self.default_value
        if current_value is not None:
            self.current_value = current_value

    @property
    def current_value(self) -> str:
        if not self.current_value_str:
            return None
        return self.type_filter.from_string(value = self.current_value_str)

    @current_value.setter
    def current_value(self, value):
        if self.type_filter.check(value):
            self.current_value_str = self.type_filter.to_string(value)

    def get_path(self) -> str:
        return f"{str(self.scope)}:{self.topic}.{self.setting_id}"