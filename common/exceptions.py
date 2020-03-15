class BeitrisError(Exception):
    msg = 'Unknown error'
    code = 500

    def __init__(self):
        msg = getattr(self.__class__, 'msg')
        code = getattr(self.__class__, 'code')
        super().__init__(code, msg)


class WikidataSparQLError(BeitrisError):
    msg = 'Unexpected error while request to Wikidata'


class WikidataResultError(BeitrisError):
    msg = 'Unexpected result from Wikidata'


class BackendDoesNotExist(BeitrisError):
    msg = 'Backend does not exist'
    code = 404


class FileTypeError(BeitrisError):
    msg = 'File type not allowed'
    code = 404


class NotFoundError(BeitrisError):
    msg = 'File type not allowed'
    code = 404


class RoomPermissionsDenied(BeitrisError):
    msg = "You don't have permissions to this room"
    code = 403


class RoomNotFound(BeitrisError):
    msg = "Room does not exist"
    code = 404


class GamePermissionsDenied(BeitrisError):
    msg = "You don't have permission to this game"
    code = 403
