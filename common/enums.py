import enum


class BeitrisEnum(enum.Enum):
    @classmethod
    def values(cls):
        return [x.value for x in cls]

    @classmethod
    def to_choices(cls):
        return ((x.name, x.value) for x in cls)


class Backends(BeitrisEnum):
    telegram = 'telegram'
    api = 'api'


class QuestionTypes(BeitrisEnum):
    image = 'image'
    text = 'text'
    sounds = 'sounds'
    coords = 'coords'


class MessageTypes(BeitrisEnum):
    info = 'INFO'
    success = 'SUCCESS'
    warning = 'WARNING'
    error = 'ERROR'
