class BeitrisError(Exception):
    def __init__(self):
        msg = getattr(self.__class__, 'msg', 'Unknown Error')
        code = getattr(self.__class__, 'code', 500)
        super().__init__(code, msg)


class WikidataSparQLError(BeitrisError):
    msg = 'Unexpected error while request to Wikidata'


class WikidataResultError(BeitrisError):
    msg = 'Unexpected result from Wikidata'


class BackendDoesNotExist(BeitrisError):
    msg = 'Backend does not exist'


class FileTypeError(BeitrisError):
    msg = 'File type not allowed'
    code = 404


class NotFoundError(BeitrisError):
    msg = 'File type not allowed'
    code = 404
