class Item:
    def __init__(self):
        self.name = None
        self.descriptionRectangle = None
        self.description = None
        self.columns = None
        self.rows = None
        self.parent = None
        self.soulBound = None
        self.accessLocation = None
        self.yoloClassName = None

    # Get
    def getAccessLocation(self):
        return self.accessLocation

    def getYoloClassName(self):
        return self.yoloClassName

    def getColumns(self):
        return self.columns

    def getDescription(self):
        return self.description

    def getDescriptionRectangle(self):
        return self.descriptionRectangle

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getRows(self):
        return self.rows

    def getSoulBound(self):
        return self.soulBound

    # Set
    def setAccessLocation(self, rectangle):
        self.accessLocation = rectangle

    def setYoloClassName(self, yoloClassName):
        self.yoloClassName = yoloClassName

    def setColumns(self, columns):
        self.columns = columns

    def setDescription(self, list):
        self.description = list

    def setDescriptionRectangle(self, rectangle):
        self.descriptionRectangle = rectangle

    def setName(self, name):
        self.name = name

    def setParent(self, parent):
        self.parent = parent

    def setRows(self, rows):
        self.rows = rows

    def setSoulbound(self, boolean):
        self.soulBound = boolean
