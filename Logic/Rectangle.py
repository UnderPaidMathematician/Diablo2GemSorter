class Rectangle:
    def __init__(self):
        self.topLeftLocation = None
        self.width = None
        self.height = None
        self.bottomRightLocation = None
        self.centerLocation = None

    # Get
    def getBottomRightLocation(self):
        return self.bottomRightLocation

    def getCenterLocation(self):
        return self.centerLocation

    def getHeight(self):
        return self.height

    def getTopLeftLocation(self):
        return self.topLeftLocation

    def getWidth(self):
        return self.width

    # Set
    def setBottomRightLocation(self):
        if self.topLeftLocation is None or self.width is None or self.height is None:
            print("Rectangle Failed to get Bottom Right location")
        else:
            self.bottomRightLocation = (self.topLeftLocation[0] + self.width + 1, self.topLeftLocation[1] + self.height + 1)

    def setCenterLocation(self):
        if self.topLeftLocation is None or self.width is None or self.height is None:
            print("Rectangle Failed to get Bottom Right location")
        else:
            self.centerLocation = (self.topLeftLocation[0] + self.width*.5, self.topLeftLocation[1] + self.height*.5)

    def setHeight(self, height):
        self.height = height

    def setTopLeftLoction(self, x, y):
        self.topLeftLocation = (x, y)

    def setWidth(self, width):
        self.width = width
