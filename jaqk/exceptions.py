class JAQKException(Exception):

    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url', None)
        self.company = kwargs.pop('company', None)
        self.sheet = kwargs.pop('sheet', None)
        super(JAQKException, self).__init__(*args, **kwargs)

# Huge potential later
# All exceptions and "checking" will come from here

class GetterRequestError(JAQKException):
    pass

    '''
    def __init__(self, *args, **kwargs):
        super(GetterRequestError, self).__init__(*args, **kwargs)
        #self.msg = "Failed to request url {}"
    def __str__(self):
        return "Failed to request url {}".format(self.url)
'''


class TransInternetError(JAQKException):
    pass