class Flag():
    def __init__(self):
        self._chainfill = False
        self._halfhaerted = False
        self._loop = False
        self._end = False
        self._count = None
        self.__cell = None, None

    # ----------------------------
    def getChainFill(self):
        return self._chainFill

    def setChainFill(self, value:bool):
        self._chainFill = value
    # ----------------------------
    def getHalfhaerted(self):
        return self._halfhaerted

    def setHalfhaerted(self, value:bool):
        self._halfhaerted = value
    # ----------------------------
    def getHalfOpen(self):
        return self._loop

    def setHalfOpen(self, value:bool):
        self._loop = value
    # ----------------------------
    def getEnd(self):
        return self._end
    
    def setEnd(self, value:bool):
        self._end = value
    # ----------------------------
    def setCount(self, value:int):
        self._count = value
        
    def getCount(self):
        return self._count
    # ----------------------------
    def getCell(self):
        return self._cell

    def setCell(self, u, v):
        self._cell = u, v