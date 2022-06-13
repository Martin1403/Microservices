

class AsyncTest(object):
    """Async Class"""
    def __init__(self):
        self.text = "Async test ok..."

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def __await__(self):
        return self.__aenter__().__await__()
