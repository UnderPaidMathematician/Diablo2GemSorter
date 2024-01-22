from Item import Item

class InventorySlot:
    def __init__(self):
        self.item = None
        self.parent = None
        self.accessLocation = None
        self.slotId = None

    # Get
    def getSlotId(self):
        return self.slotId

    def getItem(self):
        return self.item

    def getAccessLocation(self):
        return self.accessLocation

    def getParent(self):
        return self.parent

    # Set
    def setSlotId(self, slotId):
        self.slotId = slotId

    def setItem(self, item):
        self.item = item

    def setAccessLocation(self, rectangle):
        self.accessLocation = rectangle

    def setParent(self, container):
        self.parent = container





