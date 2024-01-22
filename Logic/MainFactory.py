from Containers import Containers
from Rectangle import Rectangle
from InventorySlot import InventorySlot


class MainFactory:
    @staticmethod
    def buildContainers():

        # Access locations
        stashAccessRectangle0 = Rectangle()
        stashAccessRectangle1 = Rectangle()
        stashAccessRectangle2 = Rectangle()
        stashAccessRectangle3 = Rectangle()

        stashAccessRectangle0.setTopLeftLoction(323, 374)
        stashAccessRectangle1.setTopLeftLoction(571, 374)
        stashAccessRectangle2.setTopLeftLoction(820, 374)
        stashAccessRectangle3.setTopLeftLoction(1069, 374)

        stashAccessRectangle0.setWidth(239)
        stashAccessRectangle1.setWidth(241)
        stashAccessRectangle2.setWidth(241)
        stashAccessRectangle3.setWidth(241)

        stashAccessRectangle0.setHeight(61)
        stashAccessRectangle1.setHeight(61)
        stashAccessRectangle2.setHeight(61)
        stashAccessRectangle3.setHeight(61)

        stashAccessRectangle0.setCenterLocation()
        stashAccessRectangle1.setCenterLocation()
        stashAccessRectangle2.setCenterLocation()
        stashAccessRectangle3.setCenterLocation()

        stashAccessRectangle0.setBottomRightLocation()
        stashAccessRectangle1.setBottomRightLocation()
        stashAccessRectangle2.setBottomRightLocation()
        stashAccessRectangle3.setBottomRightLocation()

        # setup default container values
        containerDefautValueDict = [
            {
                'name': "Shared 0",
                'rows': 10,
                'columns': 10,
                'accessLocation': stashAccessRectangle0,
                'allowSoulBoundItems': True
            },

            {
                'name': "Shared 1",
                'rows': 10,
                'columns': 10,
                'accessLocation': stashAccessRectangle1,
                'allowSoulBoundItems': False
            },

            {
                'name': "Shared 2",
                'rows': 10,
                'columns': 10,
                'accessLocation': stashAccessRectangle2,
                'allowSoulBoundItems': False
            },

            {
                'name': "Shared 3",
                'rows': 10,
                'columns': 10,
                'accessLocation': stashAccessRectangle3,
                'allowSoulBoundItems': False
            },

            {
                'name': "Inventory",
                'rows': 4,
                'columns': 10,
                'accessLocation': None,
                'allowSoulBoundItems': True
            },

            {
                'name': "Horadric Cube",
                'rows': 4,
                'columns': 3,
                'accessLocation': None,
                'allowSoulBoundItems': False
            }
        ]

        # Build my list of containers.
        containerList = []
        slotCounter = 0

        # build my side lengths and padding
        itemSideLength = 97
        padding = 1

        # get default values for containers
        for numberOfContainers, defaultValues in enumerate(containerDefautValueDict):

            # build containers and append to list
            containerList.append(Containers(defaultValueDict=defaultValues))

            # build a new list for each container
            inventorySlotList = []

            # 0-3 are stash containers, 4 is inventory, and 5 is the horadric cube.
            currentContainerRectangle = Rectangle()
            if numberOfContainers < 4:
                currentContainerRectangle.setTopLeftLoction(325, 443)
                currentContainerRectangle.setWidth(980)
                currentContainerRectangle.setHeight(980)
            elif numberOfContainers == 4:
                currentContainerRectangle.setTopLeftLoction(2536, 1105)
                currentContainerRectangle.setWidth(980)
                currentContainerRectangle.setHeight(392)
            elif numberOfContainers == 5:
                currentContainerRectangle.setTopLeftLoction(667, 744)
                currentContainerRectangle.setWidth(294)
                currentContainerRectangle.setHeight(392)

            newRow = 0
            # build inventory slots append to list
            for s in range(0, defaultValues['columns'] * defaultValues['rows']):
                inventorySlotList.append(InventorySlot())

                # set the inventory ID for the slot
                inventorySlotList[-1].setSlotId(slotCounter)
                slotCounter += 1

                # Setup slots accessLocation
                currentRectangle = Rectangle()
                currentRectangle.width = itemSideLength
                currentRectangle.height = itemSideLength

                topLeftX, topLeftY = currentContainerRectangle.getTopLeftLocation()

                if s % (defaultValues['columns']) == 0:
                    newRow += 1

                x = topLeftX + (s % (defaultValues['columns'])) * currentRectangle.getWidth() + (
                        s % (defaultValues['columns'])) * padding
                y = topLeftY + (newRow - 1) * currentRectangle.getHeight() + (newRow - 1) * padding


                # Set the top left, bottom right, and center
                currentRectangle.setTopLeftLoction(x, y)
                currentRectangle.setBottomRightLocation()
                currentRectangle.setCenterLocation()

                # set the container as the parent
                inventorySlotList[-1].setParent(containerList[-1])

                inventorySlotList[-1].setAccessLocation(currentRectangle)

            containerList[-1].setInventorySlotList(inventorySlotList)

        return containerList
