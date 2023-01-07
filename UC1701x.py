#this script is write for JLX12864G-1353-BN, with some change may com
#
from micropython import const
import framebuf

SET_COLADD_L=const(0x00)#set [3:0] of column address reg |0x0X X from 0 to F
SET_COLADD_H=const(0x10)#set [7:4] of column address reg |0x0X X from 0 to 8  (0x00-0x83 (132 in total))
SET_PWR_CTRL=const(0x28)#set power control reg |0x0X X from 0 to 7
SET_SCROLL_LINE=const(0x40)#scroll screen for 0 to 63 line |0xXX XX from 0 to 3F
SET_PAGE_ADD=const(0xB0)#set 4 bit page address reg |0x0X X from 0 to 8 (0 to 7 in normal disp, 8th page isn't support in my display)
VLCD_R_RATIO=const(0x20)#set bias PC[5:3] |0x0X X from 0 to 7 (rough tune contrast)
CONTRAST_SET=const(0x81)#adjust contrast command, MUST followed by a byte from 0x00 to 0x3F (fine tune contrast)
ALL_PIX_ON=const(0xA4)#|0x01 or 0x00
SET_INV_DISP=const(0xA6)#|0x01 or 0x00
SET_ENA_DISP=const(0xAE)#|0x01 or 0x00 enable display, 0(OFF) BY DEFAULT! set to 0 will set chip in sleep mode
SET_SEG_DIR_=const(0xA0)#|0x01 or 0x00 invX use 0xA0
SET_COM_DIR_=const(0xC0)#|0x08 or 0x00 invY use 0xC8
SYS_SOFT_RST=const(0xE2)
BIAS_RATIO=const(0xA2)#|0x01 or 0x00 (0x00 (1/9) is used in my screen)
SET_CUR_UPDT=const(0xE0)#increment column address when write data
#RST_CUR_UPDT=const(0xEE)#not used
#SET_STAT_OFF=const(0xAC)#set static indicator
#SET_STAT_ON_=const(0xAD)#
#BOOST_RATIO_=const(0xF8)#MUST FOLLOWED BY 0x00~0x03 my screen don't need this(0x00)

class UC1701x(framebuf.FrameBuffer):
    def __init__(self,spi,a0,rst=None,cs=None,roughContrast=0x03,fineContrast=0x28,invX=False,invY=False,invDISP=False):
        self.spi=spi
        a0.init(a0.OUT,value=0)
        self.a0=a0#1:data 0:command
        self.existCS=False
        if(cs is not None):
            self.existCS=True
            cs.init(cs.OUT,value=0)
            self.cs=cs
        #self.existRST=False
        if(rst is not None):
            #self.existRST=True
            import time
            time.sleep_ms(10)
            rst.init(rst.OUT,value=0)
            self.rst=rst
            time.sleep_ms(10)
            self.rst(1)
            time.sleep_ms(100)
        else:
            import time
            time.sleep_ms(10)
            self.writeCMD(SYS_SOFT_RST);
            time.sleep_ms(100)
        self.buffer=bytearray(128*64//8)
        super().__init__(self.buffer, 128, 64, framebuf.MONO_VLSB)
        self.writeCMD(SET_PWR_CTRL|0x04)
        time.sleep_ms(5)
        self.writeCMD(SET_PWR_CTRL|0x06)
        time.sleep_ms(5)
        self.writeCMD(SET_PWR_CTRL|0x07)
        time.sleep_ms(5)
        self.writeCMD(VLCD_R_RATIO|roughContrast)
        self.writeCMD(CONTRAST_SET)
        self.writeCMD(fineContrast)
        self.writeCMD(BIAS_RATIO|0x00)#for my screen only
        if(invY):
            self.writeCMD(SET_COM_DIR_|0x08)
        else:
            self.writeCMD(SET_COM_DIR_)#|0x00
        if(invX):
            self.writeCMD(SET_SEG_DIR_|0x01)
        else:
            self.writeCMD(SET_SEG_DIR_)
        if(invDISP):
            self.writeCMD(SET_INV_DISP|0x01)
        else:
            self.writeCMD(SET_INV_DISP)
        #self.writeCMD(SET_COLADD_H)#|0x00)
        #self.writeCMD(SET_COLADD_L)#|0x00)
        #self.writeCMD(SET_PAGE_ADD)
        self.writeCMD(SET_CUR_UPDT)
        pagcnt=0
        while (pagcnt<9):
            self.writeCMD(SET_COLADD_H)#|0x00)
            self.writeCMD(SET_COLADD_L)#|0x00)
            self.writeCMD(SET_PAGE_ADD|pagcnt)
            self.writeDATA(bytearray([0 for cnt in range(0,132)]))
            pagcnt+=1
        self.writeCMD(SET_ENA_DISP|0x01)
        #self.writeCMD(SET_SCROLL_LINE)#|0x00)
        if(cs is not None):
            self.cs(1)
    
    def writeCMD(self,cmd):
        if(self.existCS):
            self.cs(0)
        self.a0(0)
        self.spi.write(bytearray([cmd]))
        if(self.existCS):
            self.cs(1)
        
    def writeDATA(self,databuf):
        if(self.existCS):
            self.cs(0)
        self.a0(1)
        self.spi.write(databuf)
        if(self.existCS):
            self.cs(1)
        
    def ALLPIXON(self,switch):
        self.writeCMD(ALL_PIX_ON|switch)
        
    def sleep(self):
        self.writeCMD(SET_ENA_DISP)#|0x00)
        self.ALLPIXON(0x01)
        
    def wakeup(self):
        self.ALLPIXON(0x00)
        self.writeCMD(SET_ENA_DISP|0x01)
        
    def scrolLine(self,numofLine):
        self.writeCMD(SET_SCROLL_LINE|numofLine)
        
    def show(self):
        #colcnt=0
        #self.writeCMD(SET_ENA_DISP|0x00)
        #self.writeCMD(SET_SCROLL_LINE)
        pagcnt=0
        while(pagcnt<8):
            self.writeCMD(SET_COLADD_H)#|0x00)
            self.writeCMD(SET_COLADD_L)#|0x00)
            self.writeCMD(SET_PAGE_ADD|pagcnt)
            self.writeDATA(self.buffer[(128*pagcnt):(128*pagcnt+128)])
            self.writeDATA(bytearray([0,0,0,0]))
            pagcnt+=1
        #self.writeCMD(SET_ENA_DISP|0x01)