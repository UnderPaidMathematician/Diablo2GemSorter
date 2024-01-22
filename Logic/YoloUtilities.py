import pyautogui

from Utilities import Utilities
from MouseUtilities import MouseUtilities
import os
from Rectangle import Rectangle


class YoloUtilities:
    YOLO_TRAINING_PATH = r"C:\PythonProjects\DiabloGemSorterOOP\Data\YoloTraining"
    YOLO_TRAINING_FILE_NAME = "_DiabloYoloTraining.png"

    # Rectangle used to avoid text popups can be used to move mouse to upper left corner.
    DEFAULT_RECTANGLE = Rectangle()
    DEFAULT_RECTANGLE.setWidth(3)
    DEFAULT_RECTANGLE.setHeight(3)
    DEFAULT_RECTANGLE.setTopLeftLoction(0, 0)
    DEFAULT_RECTANGLE.setBottomRightLocation()
    DEFAULT_RECTANGLE.setCenterLocation()

    @staticmethod
    def assignYoloClassNamesToItems(fullInventoryList, yoloClassNames):
        for item in fullInventoryList:
            for yoloName in yoloClassNames:
                if item.getName().split(" ") == yoloName.split("_")[1:]:
                    item.setYoloClassName(yoloName)

                splitName = item.getName().split(" ")
                isJewel = False
                for i in splitName:
                    if i == "JEWEL":
                        isJewel = True

                if isJewel and "JEWEL" == yoloName.split("_")[-1]:
                    item.setYoloClassName(yoloName)

        unassignedItems = [x for x in fullInventoryList if x.getYoloClassName() is None]
        if len(unassignedItems) == 0:
            print("Successfully Assigned Class Names to all Items.")
        else:
            # TODO Fuzzy matching if we find that the OCR is making mistakes
            print(f"Failed to assign class names to: {unassignedItems}")

    @staticmethod
    def buildYoloImages(sourceEnabledContainers):
        # gets the access rectangles for the containers
        accessLocationList = [x.getAccessLocation() for x in sourceEnabledContainers]

        # Gets the latest image
        counter = YoloUtilities.findCurrentCounter()

        fileNameList = []
        for location in accessLocationList:
            if location is not None:
                MouseUtilities.MoveMouseToRectangle(location)
                MouseUtilities.MouseLeftClick()
                MouseUtilities.MoveMouseToRectangle(YoloUtilities.DEFAULT_RECTANGLE, isCenters=True)

                fileName = f"{counter}{YoloUtilities.YOLO_TRAINING_FILE_NAME}"
                Utilities.ScreenToDisk(YoloUtilities.YOLO_TRAINING_PATH, fileName)
                fileNameList.append(fileName)
                counter += 1

        return fileNameList


    @staticmethod
    def buildYoloBoxFiles(fileNameList, fullInventoryList, sourceEnabledContainers):
        # We know that each file name is associated with the access location list.
        accessLocationList = [x.getAccessLocation() for x in sourceEnabledContainers]

        # Follows the same initial format as Build Yolo Images
        for i, location in enumerate(accessLocationList):
            # each location would have its own set of items that it needs to track.
            currentImageItemList = []
            if location is not None:
                # Checks the items to see if they are in the current image.
                # If they do belong it collects the item.
                for item in fullInventoryList:
                    if id(item.getParent().getParent().getAccessLocation()) == id(location):
                        currentImageItemList.append(item)
            else:
                # All Locations can see the inventory container
                # If access location is None but the parent container is Inventory track it.
                for item in fullInventoryList:
                    if item.getParent().getParent().getName() == "Inventory":
                        currentImageItemList.append(item)

            # Write the yoloTextFile
            # build accessLocation
            # Normalize accessLocation
            for item in currentImageItemList:
                # If the item only fills one inventory slot use the current accessLocation for inventory slot.
                if item.getColumns() == 1 and item.getRows() == 1:
                    itemRectangle = item.getParent().getAccessLocation()
                else:
                    inventorySlotList = item.getParent().getParent().getInventorySlotList()
                    slotsCoveredByItem = [x for x in inventorySlotList if id(x.getItem()) == id(item)]

                    topLeftSlot = slotsCoveredByItem[0]
                    bottomRightSlot = slotsCoveredByItem[0]
                    for slot in slotsCoveredByItem:
                        if slot.getSlotId() < topLeftSlot.getSlotId():
                            topLeftSlot = slot

                        if slot.getSlotId() > bottomRightSlot.getSlotId():
                            bottomRightSlot = slot

                    width = abs(topLeftSlot.getAccessLocation().getTopLeftLocation()[0] - bottomRightSlot.getAccessLocation().getBottomRightLocation()[0])
                    height = abs(topLeftSlot.getAccessLocation().getTopLeftLocation()[1] - bottomRightSlot.getAccessLocation().getBottomRightLocation()[1])

                    itemRectangle = Rectangle()
                    itemRectangle.setWidth(width)
                    itemRectangle.setHeight(height)
                    itemRectangle.setTopLeftLoction(topLeftSlot.getAccessLocation().getTopLeftLocation()[0], topLeftSlot.getAccessLocation().getTopLeftLocation()[1])
                    itemRectangle.setBottomRightLocation()
                    itemRectangle.setCenterLocation()

                normalRectangle = YoloUtilities.NormalizeRectangle(itemRectangle)

                with open(f"C:\PythonProjects\DiabloGemSorterOOP\Data\YoloTraining\{fileNameList[i][:-4]}.txt", "a") as file:
                    file.write(f"{item.getYoloClassName().split('_')[0]} {normalRectangle.getCenterLocation()[0]} {normalRectangle.getCenterLocation()[1]} {normalRectangle.getWidth()} {normalRectangle.getHeight()}\n")



    @staticmethod
    def buildYoloTrainingFiles(sourceEnabledContainers, destinationContainers, fullInventoryList):
        fileNameList = YoloUtilities.buildYoloImages(sourceEnabledContainers)

        # TODO Only used once to build the classes. (You must account for changes in classes)
        # YoloUtilities.setYoloClasses(fullInventoryList, saveToFile=True)

        yoloClassNames = YoloUtilities.getYoloClasses()

        YoloUtilities.assignYoloClassNamesToItems(fullInventoryList, yoloClassNames)

        YoloUtilities.buildYoloBoxFiles(fileNameList, fullInventoryList, sourceEnabledContainers)

    @staticmethod
    def getYoloClasses():
        with open(r"C:\PythonProjects\DiabloGemSorterOOP\Data\yoloClassesMasterList.txt", "r") as file:
            classListUnCleaned = file.readlines()
            cleanedClassList = [x.replace("\n", "") for x in classListUnCleaned]

        return cleanedClassList

    @staticmethod
    def findCurrentCounter():
        fileList = []
        for dirpath, subdirs, files in os.walk(YoloUtilities.YOLO_TRAINING_PATH):
            pass

        for file in files:
            if file[-3:] == "png":
                fileList.append(int(file.split("_")[0]))

        return len(fileList)

    @staticmethod
    def NormalizeRectangle(rectangle):
        xRez, yRez = pyautogui.size()

        rectangle.setWidth(abs(rectangle.getBottomRightLocation()[0] - rectangle.getTopLeftLocation()[0])/xRez)
        rectangle.setHeight(abs(rectangle.getBottomRightLocation()[1] - rectangle.getTopLeftLocation()[1])/yRez)
        rectangle.setTopLeftLoction(rectangle.getTopLeftLocation()[0]/xRez, rectangle.getTopLeftLocation()[1]/yRez)
        rectangle.setBottomRightLocation()
        rectangle.setCenterLocation()

        return rectangle

    @staticmethod
    def setYoloClasses(fullInventoryList, saveToFile=False):
        """
        This is used to set the classes.
        Used only once to build the file.
        There were a total of 39 classes created.
        They all must be accounted for in the Yolo Build.
        Dont run this unless you know what you are doing.
        """
        allClassNames = [x.getName() for x in fullInventoryList]

        # Jewels come in many flavors but they are still just one class
        jewelFixClassNames = []
        for itemName in allClassNames:
            foundJewel = False

            itemNameList = itemName.split(" ")

            for i in itemNameList:
                if i == "JEWEL":
                    foundJewel = True

            if foundJewel:
                jewelFixClassNames.append("JEWEL")
            else:
                jewelFixClassNames.append(itemName.replace(" ", "_"))

        classNames = set(jewelFixClassNames)

        classNames = sorted(classNames)
        classNamesList = []
        for name in classNames:
            classNamesList.append(name)

        # I want my classes in a specific order for the gems. This will aid later in troubleshooting
        classTypeOrder = ['AMETHYST', 'DIAMOND', 'EMERALD', 'RUBY', 'SAPPHIRE', 'SKULL', 'TOPAZ', 'CUBE', 'IDENTIFY',
                          'JEWEL', 'PORTAL']
        gemQualityOrder = ['CHIPPED', 'FLAWED', '', 'FLAWLESS', 'PERFECT']
        classResultsSorted = []
        for classType in classTypeOrder:
            for gemQuality in gemQualityOrder:
                for item in classNamesList:

                    if item.split("_")[0] == gemQuality and item.split("_")[-1] == classType:
                        classResultsSorted.append(item)
                        if gemQuality == "FLAWED":
                            classResultsSorted.append(classType)

        # Here I gather anything that was not found in the logic above and add those classes to the end of the list
        missingItems = list(set(classNamesList).difference(classResultsSorted))
        for i in missingItems:
            classResultsSorted.append(i)

        if saveToFile == True:
            '''Note You must account for these classes in the yolo setup. '''
            with open(r"C:\PythonProjects\DiabloGemSorterOOP\Data\yoloClassesMasterList.txt", "w") as file:
                for i, c in enumerate(classResultsSorted):
                    file.write(f"{i}_{c}\n")



