from os import environ

"""
Environment:
Set default environment, if environment not seted
Override default environment, if environment seted
Allowed types: string, list, integer, float
"""


class EnvironmentMustBeSetException(BaseException):
    pass


class Environment:
    def __init__(self, key, default):
        self.key = key
        self.default = default

    def get_string(self):
        try:
            value = environ[self.key]
            if value is None or value == "":
                raise KeyError
            return value
        except KeyError:
            if self.default is None or self.default == "":
                raise EnvironmentMustBeSetException
            return self.default


class EnvironmentBoolean(Environment):
    def get_bool(self):
        string = self.get_string()
        if type(string) == bool:
            return string
        if string.lower() == "true":
            return True
        elif string.lower() == "false":
            return False
        else:
            raise ValueError(f"{self.key} is bool, but not true or false")


class EnvironmentList(Environment):
    def get_list(self):
        string = self.get_string()
        if type(string) == list:
            return string
        l = string.split(",")
        return l


class EnvironmentInteger(Environment):
    def get_int(self):
        string = self.get_string()
        if type(string) == int:
            return string
        i = int(string)
        return i


class EnivronmentFloat(Environment):
    def get_float(self):
        string = self.get_string()
        if type(string) == float:
            return string
        i = float(string)
        return i
