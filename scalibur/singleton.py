class _Singleton:
    _singletons = {}

    @staticmethod
    def apply(cls):
        print("[_Singleton] apply")
        if cls not in _Singleton._singletons:
            _Singleton._singletons[cls] = _Singleton(cls)
        return _Singleton._singletons[cls]

    def __init__(self, cls):
        print("[_Singleton] __init__")
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        print("[_Singleton] __call__")
        if self._instance is None:
            self._instance = self._cls(*args, **kwargs)
        return self._instance


def singleton(cls):
    return _Singleton.apply(cls)
