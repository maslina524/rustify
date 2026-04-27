class UnwrappingErr(Exception):
    def __init__(self, err: str):
        super().__init__(err)
        self._err = err