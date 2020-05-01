import enum

from common.exceptions import BeitrisError


class ForceDisconnect(Exception):
    pass


class AnotherClientConnected(BeitrisError):
    msg = 'Another client connected using this credentials'


class UnexpectedCommand(BeitrisError):
    msg = 'Unexpected command'
    code = 400


class ParamsRequired(BeitrisError):
    msg = "'params' field is required"
    code = 400


class GameNotJoined(BeitrisError):
    msg = 'You have not joined any game'
    code = 400


class GameFinished(BeitrisError):
    msg = "Game already finished"
    code = 400


class AlreadyJoined(BeitrisError):
    msg = "You have already joined this game"
    code = 400


# TODO: rework enum to exceptions
class WebsocketErrors(enum.Enum):
    ERROR_3001 = ('critical', 3001, 'Another client connected using this credentials')