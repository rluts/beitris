import enum


class ForceDisconnect(Exception):
    pass


class WebsocketErrors(enum.Enum):
    ERROR_3001 = ('critical', 3001, 'Another client connected using this credentials')
    ERROR_3002 = ('error', 3002, 'Unexpected command')
    ERROR_3003 = ('error', 3003, "'params' field is required")

    ERROR_3004 = ('error', 3004, 'You have not joined any game')