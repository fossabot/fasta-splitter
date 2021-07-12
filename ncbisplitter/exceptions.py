class Error(Exception):
    pass


class InvalidExtensionFileError(Error):
    pass


class InvalidFormattedFastaFileError(Error):
    pass


class InvalidNumberofArgumentsError(Error):
    pass
