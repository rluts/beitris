import enum


class BeitrisEnum(enum.Enum):
    @classmethod
    def values(cls):
        return [x.value for x in cls]


class Backends(BeitrisEnum):
    telegram = 'telegram'
    api = 'api'
