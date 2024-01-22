import cv2
from MouseUtilities import MouseUtilities
import numpy as np
import pyautogui
from Rectangle import Rectangle
import pytesseract
from Item import Item


class Utilities:

    @staticmethod
    def findValidCornersList():
        topBorderImage = cv2.imread(r"C:\PythonProjects\DiabloGemSorterOOP\Data\diablo_top.png")
        topBorderImage = np.copy(topBorderImage)

        leftBorderImage = cv2.imread(r"C:\PythonProjects\DiabloGemSorterOOP\Data\diablo_left.png")
        leftBorderImage = np.copy(leftBorderImage)
        # leftBorderImage = leftBorderImage.reshape((1, 95, 3))

        screenShot = Utilities.takeScreenshot()
        screenShot = np.copy(screenShot)

        pixelCheckAmount = 3
        successCounter = 0

        foundTopLeftCorner = np.where(
            (screenShot[:, :, 0] == 111) & (screenShot[:, :, 1] == 140) & (screenShot[:, :, 2] == 137))
        topLeftCornerStack = np.stack(foundTopLeftCorner, axis=1)

        validCornerList = []
        for c in topLeftCornerStack:
            successCounter = 0
            for i in range(pixelCheckAmount):
                # check horizontal
                if (np.all(screenShot[c[0] + i][c[1]]) == np.all(topBorderImage[0][i])) and \
                        (np.all(screenShot[c[0]][c[1] + i]) == np.all(leftBorderImage[i][0])):
                    successCounter += 1

            if successCounter == pixelCheckAmount:
                validCornerList.append(c)

        return validCornerList

    @staticmethod
    def getAllInventorySlots(containerList):
        listOfLists = [x.getInventorySlotList() for x in containerList].copy()

        fullInventoryList = []
        for listItem in listOfLists:
            fullInventoryList = fullInventoryList + listItem

        return fullInventoryList

    @staticmethod
    def getEnabledContainers(containterList):
        return [x for x in containterList if x.enabled is True]

    @staticmethod
    def getRowsColumns(validCorners):
        xlist = []
        ylist = []

        if len(validCorners) > 0:
            for v in validCorners:
                xlist.append(v[0])
                ylist.append(v[1])

            columns = 0
            for ux in set(xlist):
                xCount = xlist.count(ux)
                if xCount > columns:
                    columns = xCount

            rows = 0
            for uy in set(ylist):
                yCount = ylist.count(uy)
                if yCount > rows:
                    rows = yCount
        else:
            rows = None
            columns = None

        return rows, columns

    @staticmethod
    def fillInventorySlot(inventorySlot, enabledInventorySlotList, fullInventoryList):
        if inventorySlot.getItem() is None:
            # this means we did not find an item for the current inventory slot.
            pass
        else:
            # Update the master slot list if we found an item
            fullInventoryList.append(inventorySlot.getItem())

            # fill inventorySlots with items based on the size of the item we found
            # This is used to avoid checking for an item in slots that have already had their item discovered

            containerWidth = inventorySlot.getParent().getColumns()
            item = inventorySlot.getItem()

            if inventorySlot.getItem().getColumns() == 1 and inventorySlot.getItem().getRows() == 1:
                pass
            else:
                for c in range(0, inventorySlot.getItem().getColumns()):
                    slotID = inventorySlot.getSlotId() + c
                    enabledInventorySlotList[slotID].setItem(item)

                    for r in range(0, inventorySlot.getItem().getRows()):
                        rowSlotID = slotID + r * containerWidth
                        enabledInventorySlotList[rowSlotID].setItem(item)
        return fullInventoryList

    @staticmethod
    def setEnabledContainers(containerList, enabledContainersList):
        for i, container in enumerate(containerList):
            container.setEnabled(enabledContainersList[i])

    @staticmethod
    def ImageToTesseract(image):
        ocrText = pytesseract.image_to_string(image=image, lang="dia")
        return ocrText

    @staticmethod
    def ScreenToDisk(path, name, image=None):
        if image is None:
            # If there is no image take one
            image = Utilities.takeScreenshot()

        cv2.imwrite(f"{path}\\{name}", image)

    @staticmethod
    def SwapPixelColors(image, foundColor=(0, 0, 0), notFoundColor=(255, 255, 255)):
        # itemColors is a dictionary that has labels to make it easy to add or remove colors from the list
        from Data.itemColors import itemColors
        itemValues = itemColors.values()

        # openCV looks for colors in BGR so here I switch the R and B values
        diabloItemTextColors = Utilities.SwapRGBtoBGR(itemValues)

        numpyImage = image
        tabulaRasa = np.copy(numpyImage)
        tabulaRasa[:, :] = notFoundColor

        # Todo Used only for troubleshooting
        # Utilities.ScreenToDisk(r"C:\PythonProjects\DiabloGemSorterOOP\Data", "test2.png", image)

        for color in diabloItemTextColors:
            foundColorList = np.where((numpyImage[:, :, 0] == color[0]) & (numpyImage[:, :, 1] == color[1]) & (
                    numpyImage[:, :, 2] == color[2]))
            tabulaRasa[foundColorList] = foundColor

        # TODO used only for troubleshooting
        # Utilities.ScreenToDisk(r"C:\PythonProjects\DiabloGemSorterOOP\Data", "test.png", tabulaRasa)

        return tabulaRasa

    @staticmethod
    def SwapRGBtoBGR(colorList):
        bgrList = []
        for c in colorList:
            bgrList.append((c[2], c[1], c[0]))

        return bgrList

    @staticmethod
    def takeScreenshot():
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return image

    @staticmethod
    def getAllEnabledInventorySlotItems(enabledInventorySlotList,
                                        destPath=r"C:\PythonProjects\DiabloGemSorterOOP\Data\Screenshots",
                                        imgExtension="png"):

        # This is the master inventory slot list. It will have unique inventory items.
        fullInventoryList = []

        # sets the default accessLocation for access location
        currentAccessLocation = enabledInventorySlotList[0].getParent().getName()

        # Clicks the first access location
        MouseUtilities.MoveMouseToRectangle(enabledInventorySlotList[0].getParent().getAccessLocation())
        MouseUtilities.MouseLeftClick()

        for inventorySlot in enabledInventorySlotList:

            # If the inventory slot is linked to others skip it
            if inventorySlot.getItem() != None:
                continue

            # If the access location does not match save the new location and click the access location
            if inventorySlot.getParent().getName() != currentAccessLocation \
                    and inventorySlot.getParent().getAccessLocation() is not None:
                currentAccessLocation = inventorySlot.getParent().getName()
                MouseUtilities.MoveMouseToRectangle(inventorySlot.getParent().getAccessLocation())
                MouseUtilities.MouseLeftClick()

            # Move Mouse
            MouseUtilities.MoveMouseToRectangle(rectangle=inventorySlot.getAccessLocation(), isCenters=True)

            # save screenshot to disk
            name = f"{inventorySlot.getSlotId()}_{inventorySlot.getParent().getName()}.{imgExtension}"

            # TODO troubleshooting only
            # Utilities.ScreenToDisk(destPath, name)

            # We know that the center of the inventory slot is either above or below the description box
            # We could have just scanned the entire image from top to bottom but this will be much faster.
            centerX, centerY = inventorySlot.getAccessLocation().centerLocation
            centerX = int(centerX)
            centerY = int(centerY)
            image = Utilities.takeScreenshot()

            # takes the cursor location and moves up and down trying to find the item window
            upLocation = centerY
            downLocation = centerY + 1

            # tracking the rows that we find
            rowLocation = []

            # Using bitwise mask
            UP = 2  # 0000 0010
            DOWN = 4  # 0000 0100
            BOTH = 6  # 0000 0110 (the bits line up to include 2 and 4)

            # At first we dont know if we will find the description box above or below the cursor
            direction = BOTH

            isFinished = False

            while not isFinished:
                leftPixelCounter = 0
                rightPixelCounter = 0

                # bitwise BOTH includes both up and down since 6 has both a 2 and a 4 in it.
                # Eventually we will find whether or not the description box is above or below
                # At that time we will stop looking the other direction this should save quite a bit of processing time.
                if (direction & UP == UP) and (upLocation > -1):

                    # The color of the border we are looking for is 68,68,68
                    # I found this using the photoshop color picker.
                    if image[upLocation][centerX][0] == 68 \
                            and image[upLocation][centerX][1] == 68 \
                            and image[upLocation][centerX][2] == 68:
                        # Now I count how many times I find the color we are looking for
                        # The idea here is if I find a bunch of the same color I have run into a border
                        # Fills pixels to the left
                        for i in range(centerX, -1, -1):
                            if image[upLocation][i][0] == 68 \
                                    and image[upLocation][i][1] == 68 \
                                    and image[upLocation][i][2] == 68:
                                leftPixelCounter += 1
                            else:
                                break

                        if leftPixelCounter > 5:
                            # fills pixels to the right
                            for i in range(centerX, image.shape[1] + 1):
                                if image[upLocation][i][0] == 68 \
                                        and image[upLocation][i][1] == 68 \
                                        and image[upLocation][i][2] == 68:
                                    rightPixelCounter += 1
                                else:
                                    break

                            rowLocation.append({"yLocation": upLocation, "width": leftPixelCounter + rightPixelCounter})
                            direction = UP

                upLocation -= 1

                if (direction & DOWN == DOWN) and (downLocation < image.shape[0]):
                    if image[downLocation][centerX][0] == 68 \
                            and image[downLocation][centerX][1] == 68 \
                            and image[downLocation][centerX][2] == 68:
                        for i in range(centerX, -1, -1):
                            if image[downLocation][i][0] == 68 \
                                    and image[downLocation][i][1] == 68 \
                                    and image[downLocation][i][2] == 68:
                                leftPixelCounter += 1
                            else:
                                break

                        if leftPixelCounter > 5:
                            for i in range(centerX, image.shape[1] + 1):
                                if image[downLocation][i][0] == 68 \
                                        and image[downLocation][i][1] == 68 \
                                        and image[downLocation][i][2] == 68:
                                    rightPixelCounter += 1
                                else:
                                    break
                            rowLocation.append(
                                {"yLocation": downLocation, "width": leftPixelCounter + rightPixelCounter})
                            direction = DOWN

                downLocation += 1

                # No descriptions were found
                if (upLocation < 0) and (downLocation > image.shape[0]):
                    isFinished = True

                # We found a description above our cursor
                if direction == UP and len(rowLocation) == 3:
                    # Build an item
                    inventorySlot.setItem(Item())

                    # build descriptionRectangle
                    rectangle = Rectangle()
                    rectangle.setTopLeftLoction(centerX - leftPixelCounter, rowLocation[-1]["yLocation"])
                    rectangle.setWidth(rowLocation[-1]["width"])
                    rectangle.setHeight(abs(rowLocation[-1]["yLocation"] - (rowLocation[-2]["yLocation"])))
                    rectangle.setBottomRightLocation()
                    rectangle.setCenterLocation()

                    # Set description accessLocation
                    inventorySlot.getItem().setDescriptionRectangle(rectangle)

                    # Save a cropped image for testing purposes
                    descriptionX1, descriptionY1 = rectangle.getTopLeftLocation()
                    descriptionX2, descriptionY2 = rectangle.getBottomRightLocation()

                    croppedImage = image[descriptionY1:descriptionY2, descriptionX1:descriptionX2]
                    name = f"{inventorySlot.getSlotId()}_{inventorySlot.getParent().getName()}_cropped.{imgExtension}"

                    # pixel color swap turn image into fully black and white text to preprocess image for Tesseract
                    swappedPixelImage = Utilities.SwapPixelColors(croppedImage)

                    # Cleanup text to insert into items
                    itemText = Utilities.ImageToTesseract(swappedPixelImage)
                    itemText = itemText.replace('\n\n', "\n")
                    itemText = itemText.split("\n")
                    itemText = itemText[:-1]

                    # Set the item name
                    inventorySlot.getItem().setName(itemText[0])

                    # Set the description list
                    inventorySlot.getItem().setDescription(itemText[1:])

                    # Set the parent
                    inventorySlot.getItem().setParent(inventorySlot)

                    validCorners = Utilities.findValidCornersList()
                    rows, columns = Utilities.getRowsColumns(validCorners)

                    inventorySlot.getItem().setColumns(columns)
                    inventorySlot.getItem().setRows(rows)

                    # Used for troubleshooting
                    # Utilities.ScreenToDisk(croppedPath, name, swappedPixelImage)

                    isFinished = True

                    fullInventoryList = Utilities.fillInventorySlot(inventorySlot, enabledInventorySlotList,
                                                                    fullInventoryList)

                # We found a description below our cursor
                if direction == DOWN and len(rowLocation) == 2:
                    # Build an item
                    inventorySlot.setItem(Item())

                    # build descriptionRectangle
                    rectangle = Rectangle()
                    rectangle.setTopLeftLoction(centerX - leftPixelCounter, rowLocation[-2]["yLocation"])
                    rectangle.setWidth(rowLocation[-1]["width"])
                    rectangle.setHeight(abs(rowLocation[-1]["yLocation"] - (rowLocation[-2]["yLocation"])))
                    rectangle.setBottomRightLocation()
                    rectangle.setCenterLocation()

                    # Set description accessLocation
                    inventorySlot.getItem().setDescriptionRectangle(rectangle)

                    # Save a cropped image for testing purposes
                    descriptionX1, descriptionY1 = rectangle.getTopLeftLocation()
                    descriptionX2, descriptionY2 = rectangle.getBottomRightLocation()

                    croppedImage = image[descriptionY1:descriptionY2, descriptionX1:descriptionX2]
                    name = f"{inventorySlot.getSlotId()}_{inventorySlot.getParent().getName()}_cropped.{imgExtension}"

                    # pixel color swap turn image into fully black and white text to preprocess image for Tesseract
                    swappedPixelImage = Utilities.SwapPixelColors(croppedImage)

                    # Cleanup text to insert into items
                    itemText = Utilities.ImageToTesseract(swappedPixelImage)
                    itemText = itemText.replace('\n\n', "\n")
                    itemText = itemText.split("\n")
                    itemText = itemText[:-1]

                    # Set the item name
                    inventorySlot.getItem().setName(itemText[0])

                    # Set the description list
                    inventorySlot.getItem().setDescription(itemText[1:])

                    # Set the parent
                    inventorySlot.getItem().setParent(inventorySlot)

                    validCorners = Utilities.findValidCornersList()
                    rows, columns = Utilities.getRowsColumns(validCorners)

                    inventorySlot.getItem().setColumns(columns)
                    inventorySlot.getItem().setRows(rows)

                    # Used for troubleshooting
                    # Utilities.ScreenToDisk(croppedPath, name, swappedPixelImage)

                    isFinished = True

                    fullInventoryList = Utilities.fillInventorySlot(inventorySlot, enabledInventorySlotList,
                                                                    fullInventoryList)

        return fullInventoryList


