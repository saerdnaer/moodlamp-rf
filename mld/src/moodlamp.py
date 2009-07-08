import threading        #for RLock 

class MoodlampList(list):
    lock = threading.RLock()
    def getLamp(self, lamp):
        found = False
        try:
            lamp = int(lamp)
            for l in self:
                if l.address == lamp and l.ready:
                    return l
        except ValueError:
            for l in self:
                if l.name == lamp and l.ready:
                    return l
        raise NotFound()

class DummyLamp:
    timer = 60
    address = 0
    version = "dummy"
    name = "dummy"
    ready = False
    
    def data(self, data, broadcast):
        pass
    
class Moodlamp:
    version = ''
    color = [0xff,0,0]
    done = True
    ready = False
    
    def __init__(self, interface, mld, adr, name):
        self.interface = interface
        self.mld = mld
        self.timer = 60
        self.address = adr
        self.get_version()
        self.state = 2
        self.name = name;
    
    def timer(self):
        self.tick(2, [], False)
        
    def get_address(self):
        pass
        
    def set_address(self, oldadr, newadr):
        self.mld.remove_lamp(newadr)
        self.address = newadr
        self.interface.packet(oldadr, "ADR="+chr(newadr)+self.name, 0, True)
    
    def setcolor(self, color):
        self.color = color
        self.interface.packet( self.address, "C%c%c%c" % (color[0],color[1],color[2]),0,True)
        
    def pause(self, pause):
        self.interface.packet( self.address, "\x17", 0,True)
        
    def updatefirmware(self, firmware):
        self.interface.packet( self.address,"R",0,True);
        chunkno = 0
        chunk = handle.read (pagesize)
        chunklen = len (chunk)
        while 1:
            while len (chunk) < pagesize:
                chunk = chunk + "\377"
            print "%02x (%02x): " % (chunkno, chunklen)
            #self.interface.writeflashpage(firmware)
            
    def tick(self, type, data, broadcast):
#        print "ml tick"
#        print list(data)
        if self.state == 2:
            if type == 1:
                if len(data) > 2 :
                    if data[0:2] == "D=":
                        print "processing date"
                        self.version = data[2:data.find('H=')-1]
                        self.config = data[data.find('H=')+2:]
                        self.interface.packet( self.address, "O", 0,True)
                        self.mld.new_lamp(self)
                        self.state = 3
                        self.ready = True
        elif self.state == 3:
            if len(data) > 1:
                if data[0] == 'N':
                    self.name = "".join(data[1:])
                if data[0] == 'V':
                    v = float(data[2:]) / 1024. * 2.56 * 3
                    print "voltage =", v,"V"
 
            pass
        
    def data(self, data, broadcast):
        #print "ml data:",data
        self.tick(1, data, broadcast)
        self.timer = 60
    
    def packet_done(self, broadcast):
        #print "ml done"
        self.tick(0, [], broadcast)
        
    def setraw(self, mode):
        self.interface.set_raw(mode)
        
    def setprog(self, prog):
        self.interface.packet( self.address, "\x21"+chr(prog), 0,True)
    
    def setname(self, name):
        self.interface.packet( self.address, "N"+name+"\x00", 0,True)

    def getvoltage(self):
        self.interface.packet( self.address, "K", 0,True)

    def get_version(self):
        self.interface.packet( self.address, "V", 0,True)

    def reset(self):
        self.interface.packet( self.address, "r", 0,True)

class NotFound(Exception):
    pass


