import pyautogui
import random


class MouseUtilities:

    @staticmethod
    def MoveMouseToRectangle(rectangle, isCenters=False):
        """
        Moves the mouse to accessLocation.
        isCenters = True: default to the center of the accessLocation.

        Move the mouse to randomized location in accessLocation is the default.
        """
        # hits the center points
        if isCenters:
            pyautogui.moveTo(rectangle.centerLocation)
            return

        # Random locations within the Rectangle
        buffer = 2
        x1, y1 = rectangle.getTopLeftLocation()
        x2, y2 = rectangle.getBottomRightLocation()
        xRange = range(x1 + buffer, x2 - buffer)
        yRange = range(y1 + buffer, y2 - buffer)
        pyautogui.moveTo(random.choice(xRange), random.choice(yRange))

    @staticmethod
    def MouseLeftClick():
        pyautogui.click(button='left')

