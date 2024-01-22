class Containers:
    def __init__(self, defaultValueDict):
        self.accessLocation = defaultValueDict['accessLocation']
        self.enabled = True
        self.inventorySlotList = None
        self.name = defaultValueDict['name']
        self.allowSoulBoundItems = defaultValueDict["allowSoulBoundItems"]
        self.rows = defaultValueDict["rows"]
        self.columns = defaultValueDict["columns"]
        self.isVisible = False

    # Get
    def getAccessLocation(self):
        return self.accessLocation

    def getAllowSoulBoundItems(self):
        return self.allowSoulBoundItems

    def getColumns(self):
        return self.columns

    def getEnabled(self):
        return self.enabled

    def getInventorySlotList(self):
        return self.inventorySlotList

    def getIsVisible(self):
        return self.isVisible

    def getName(self):
        return self.name

    def getRows(self):
        return self.rows

    # Set
    def setAccessLocation(self, rectangle):
        self.accessLocation = rectangle

    def setAllowSoulBoundItems(self, boolean):
        self.allowSoulBoundItems = boolean

    def setColumns(self, columns):
        self.columns = columns

    def setEnabled(self, boolEnabled):
        self.enabled = boolEnabled

    def setInventorySlotList(self, inventorySlotList):
        self.inventorySlotList = inventorySlotList

    def setIsVisible(self, boolIsVisible):
        self.isVisible = boolIsVisible

    def setName(self, name):
        self.name = name

    def setRows(self, rows):
        self.rows = rows

    @staticmethod
    def getContainer(containerList, name):
        return [x for x in containerList if x.name == name].copy()







