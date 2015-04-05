import sys
import os.path
import xbmc

class AmlogicCEC:
    def __init__(self):
	self.__cecpath = "/sys/devices/virtual/amhdmitx/amhdmitx0/cec"

    def hasCEC(self):
        return os.path.isfile(self.__cecpath)

    def __writeToCEC(self, data):
        if self.hasCEC():
            cec = open(self.__cecpath,"w")
            cec.write(data)
            cec.close()
        else:
	    xbmc.log('AmlogicCEC: CEC path %s not found' % self.__cecpath) 

    def activateSource(self):
        xbmc.log('AmlogicCEC: sending activateSource') 
        self.__writeToCEC("14");

    def deactivateSource(self):
        xbmc.log('AmlogicCEC: sending deactivateSource') 
        self.__writeToCEC("15");

    def poweronAVR(self):
        xbmc.log('AmlogicCEC: sending poweronAVR') 
        self.__writeToCEC("1b 15 40");

    def poweroffAVR(self):
        xbmc.log('AmlogicCEC: sending poweroffAVR') 
        self.__writeToCEC("1b 15 6c");

    def reportPhysicalAddress(self):
        xbmc.log('AmlogicCEC: sending report physical address') 
        self.__writeToCEC("17");
  
    def setImageviewOn(self):
        xbmc.log('AmlogicCEC: set image view on') 
        self.__writeToCEC("e");
  
class XBMCMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.__cec = kwargs['cec'];

    def onNotification(self, sender, method, data):
        xbmc.log('AmlogicCEC: got notification %s' % method) 
        if (method == 'Player.OnPlay'):
            self.__cec.poweronAVR()
            xbmc.sleep(150)
#            self.__cec.reportPhysicalAddress()
#            xbmc.sleep(100)
            self.__cec.setImageviewOn()
            xbmc.sleep(150)
            self.__cec.activateSource()

if __name__ == '__main__':
    xbmc.log('AmlogicCEC: started') 
    amlogicCEC = AmlogicCEC()
    if amlogicCEC.hasCEC():
        monitor = XBMCMonitor(cec=amlogicCEC)

        while not xbmc.abortRequested:
            xbmc.sleep(500)
    else:
	xbmc.log('AmlogicCEC: CEC not found') 

