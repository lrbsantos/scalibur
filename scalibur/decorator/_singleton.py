class _Singleton:
    _singletons = {}

    @staticmethod
    def apply(cls):
        if cls not in _Singleton._singletons:
            _Singleton._singletons[cls] = _Singleton(cls)
        return _Singleton._singletons[cls]

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance


def singleton(cls):
    return _Singleton.apply(cls)
