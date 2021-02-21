
class Type:
    __slots__ = ["name", "arguments"]

    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = tuple() if arguments is None else tuple(arguments)

    def __repr__(self):
        return f"Type({self.name}, {self.arguments})"

    def __hash__(self):
        return hash(repr(self))


class Func:
    __slots__ = ["file_path", "line_pos", "annotations", "qualifiers", "name", "parameters", "return_type"]

    def __init__(self, file_path, line_pos, annotations, qualifiers, name, parameters, return_type):
        self.file_path = file_path
        self.line_pos = line_pos
        self.annotations = annotations
        self.qualifiers = qualifiers
        self.name = name
        self.parameters = parameters
        self.return_type = return_type

    @property
    def id(self):
        return hash(f"{self.name}{self.file_path}{self.line_pos}")

    def __repr__(self):
        return f"Func({self.file_path}, {self.line_pos}, {self.annotations}, {self.qualifiers}, {self.name}, {self.parameters}, {self.return_type})"


class Param:
    __slots__ = ["name", "type_", "qualifiers"]

    def __init__(self, name, type_, qualifiers):
        self.name = name
        self.type_ = type_
        self.qualifiers = qualifiers

    def __repr__(self):
        return f"Param({self.name}, {self.type_}, {self.qualifiers})"


class Enum:
    __slots__ = ["file_path", "line_pos", "name", "members"]

    def __init__(self, file_path, line_pos, name, members):
        self.file_path = file_path
        self.line_pos = line_pos
        self.name = name
        self.members = members

    @property
    def id(self):
        return hash(f"{self.name}{self.file_path}{self.line_pos}")

    def __repr__(self):
        return f"Enum({self.file_path}, {self.line_pos}, {self.name}, {self.members})"


class EnumItem:
    __slots__ = ["name", "value"]

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"EnumItem({self.name}, {self.value})"


class Class:
    __slots__ = ["file_path", "line_pos", "qualifiers", "name", "base", "members", "is_struct"]

    def __init__(self, file_path, line_pos, qualifiers, name, base, members, is_struct=False):
        self.file_path = file_path
        self.line_pos = line_pos
        self.qualifiers = qualifiers
        self.name = name
        self.base = base
        self.members = members
        self.is_struct = is_struct

    @property
    def id(self):
        return hash(f"{self.name}{self.file_path}{self.line_pos}")

    def __repr__(self):
        return f"Class({self.file_path}, {self.line_pos}, {self.qualifiers}, {self.name}, {self.base}, {self.members}, {self.is_struct})"


class Field:
    __slots__ = ["file_path", "line_pos", "annotations", "qualifiers", "name", "type"]

    def __init__(self, file_path, line_pos, annotations, qualifiers, name, type):
        self.file_path = file_path
        self.line_pos = line_pos
        self.annotations = annotations
        self.qualifiers = qualifiers
        self.name = name
        self.type = type

    @property
    def id(self):
        return hash(f"{self.name}{self.file_path}{self.line_pos}")

    def __repr__(self):
        return f"Field({self.annotations}, {self.qualifiers}, {self.name}, {self.type})"


