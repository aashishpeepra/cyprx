import sys
from twisted.internet import reactor
import time
def destroy(bm = None):
    if bm!=None:
        bm.close()
    reactor.stop()
    print("Stopping Reactor and killing instance at ",time.time())
    sys.exit()
