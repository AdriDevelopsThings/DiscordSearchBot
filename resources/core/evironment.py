from os import environ



class EnvironmentMustBeSet(BaseException):
    pass


class EnvironmentVariable:
    def __init__(self, env_key, default=None):
        self.env_key = env_key
        self.default = default

    def call(self) -> str:
        try:
            call = environ[self.env_key]
            if call == "" or call is None:
                raise KeyError()
            return call
        except KeyError:
            if self.default is None:
                raise EnvironmentMustBeSet
            else:
                return self.default


class Version(EnvironmentVariable):
    def __init__(self):
        self.env_key = "VERSION_ENVIRONMENT"
        self.default = "v0.0"
        super().__init__(self.env_key, self.default)


class Environment(EnvironmentVariable):
    def __init__(self):
        self.env_key = "ENVIRONMENT"
        self.default = "Development"
        super().__init__(self.env_key, self.default)


def get_version_name(config):
    return f"{config.version.call()} {config.environment.call()}"
