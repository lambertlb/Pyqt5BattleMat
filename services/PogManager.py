"""
GPL 3 file header
"""
import uuid

from services.Constants import Constants
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.PogCollection import PogCollection
from services.serviceData.PogData import PogData
from services.serviceData.PogPlace import PogPlace


class PogManager:
    """
    Mange data related to Pogs
    """
    def __init__(self):
        self.baseURL = None
        self.monsterCollection = PogCollection(ReasonForAction.MonsterPogsLoaded, PogPlace.COMMON_RESOURCE)
        self.roomCollection = PogCollection(ReasonForAction.RoomObjectPogsLoaded, PogPlace.COMMON_RESOURCE)
        self.selectedPog = None

    def getMonsterCollection(self):
        return self.monsterCollection

    def getRoomCollection(self):
        return self.roomCollection

    def setSelectedPog(self, pogData):
        self.selectedPog = pogData
        ServicesManager.getEventManager().fireEvent(ReasonForAction.PogWasSelected, None)

    def getSelectedPog(self):
        return self.selectedPog

    def setPogBeingDragged(self, pogData, fromRibbonBar):
        pass

    def loadMonsterPogs(self):
        self.monsterCollection.loadFromServer(self.makeURL(Constants.ServicePath), Constants.Monsters)

    def loadRoomObjectPogs(self):
        self.roomCollection.loadFromServer(self.makeURL(Constants.ServicePath), Constants.RoomObjects)

    def makeURL(self, additions):
        """
        Mage a full url to the additions
        It assumes the base url is contained in the configuration manager
        """
        if self.baseURL is None:
            self.baseURL = ServicesManager.getConfigManager().getValue(Constants.Login_Url, 'URL')
        if not additions.startswith('/'):
            additions = '/' + additions
        return self.baseURL + additions

    def togglePlayerFlagOfSelectedPog(self, flag):
        if self.selectedPog is not None:
            self.selectedPog.togglePlayerFlag(flag)
            ServicesManager.getDungeonManager().addOrUpdatePogWithoutPlace(self.selectedPog)

    def toggleDmFlagOfSelectedPog(self, flag):
        if self.selectedPog is not None:
            self.selectedPog.toggleDmFlag(flag)
            ServicesManager.getDungeonManager().addOrUpdatePogWithoutPlace(self.selectedPog)

    def updateNumberOfSelectedPog(self, newPogNumber):
        if self.selectedPog is not None:
            self.selectedPog.setPogNumber(newPogNumber)
            ServicesManager.getDungeonManager().addOrUpdatePogWithoutPlace(self.selectedPog)

    # noinspection PyMethodMayBeStatic
    def createTemplatePog(self, pogType):
        pogData: PogData = PogData()
        pogData.uuid = str(uuid.uuid4())
        pogData.pogType = pogType
        return pogData

    # noinspection PyMethodMayBeStatic
    def getPogSizes(self):
        return ["Normal", "Large", "Huge", "Gargantuan"]
