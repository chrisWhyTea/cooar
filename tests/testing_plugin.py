from cooar.plugin import CooarPlugin


class TestingPlugin(CooarPlugin):
    def prepare(self):
        raise NotImplementedError()

    def collect(self):
        raise NotImplementedError()

    def download(self):
        raise NotImplementedError()
