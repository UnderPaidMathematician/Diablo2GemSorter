from MainFactory import MainFactory
from Utilities import Utilities
from YoloUtilities import YoloUtilities

# TODO placeholder list to be brought in with c#
enabledContainersList = [True, True, False, False, True, False]

containerlist = MainFactory.buildContainers()

Utilities.setEnabledContainers(containerlist, enabledContainersList)

SourceEnabledContainers = Utilities.getEnabledContainers(containerlist)

enabledInventoryList = Utilities.getAllInventorySlots(SourceEnabledContainers)

# TODO have C# initialize this Function
fullInventoryList = Utilities.getAllEnabledInventorySlotItems(enabledInventoryList)

destinationContainers = MainFactory.buildContainers()

Utilities.setEnabledContainers(destinationContainers, enabledContainersList)

enabledDestinationContainers = Utilities.getEnabledContainers(destinationContainers)

YoloUtilities.buildYoloTrainingFiles(SourceEnabledContainers, destinationContainers, fullInventoryList)
print("Exit")
