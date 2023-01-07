from machine import Pin,SPI
from UC1701x import UC1701x
import time

"""
__:sck is low, --:sck is high, |:sample data, x:data change, =:data hold

pha=0 pol=0 __|--__|--     pha=1 pol=0 __--|__--|__
           _x====x====                 __x====x====
pha=0 pol=1 --|__--|__     pha=1 pol=1 --__|--__|--
           _x====x====                 __x====x====

pol=0:idle state(before communication start and after communication finish) is 0
pol=1:idle state is 1

pha=0: sample at edge of first sck voltage switching
pha=1: sample at edge of second sck voltage switching
"""
spi = SPI(0,baudrate=400_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3))#under 20Mhz is OK
lcd=UC1701x(spi,cs=Pin(4),a0=Pin(1),rst=Pin(0),roughContrast=0x03,fineContrast=0x27,invX=False,invY=True)
backlight=Pin(5,Pin.OUT)
while True:
    #lcd.ALLPIXON(1)
    #time.sleep(1)
    #lcd.ALLPIXON(0)
    backlight.value(0)
    time.sleep(1)
    lcd.fill(0)
    lcd.text("ULTRACHIP",0,0,1)
    lcd.text("UC1701x demo",0,8,1)
    lcd.text("Using",0,24,1)
    lcd.text("Micro Python",0,32,1)
    lcd.text("and framebuffer",0,40,1)
    lcd.text("Code by:",0,48,1)
    lcd.text("ChangboBro",0,56,1)
    lcd.show()
    backlight.value(1)
    """cnt=0
    while(cnt<64):
        time.sleep_ms(100)
        lcd.scrolLine(2)
        cnt+=2
        time.sleep_ms(100)
        lcd.scrolLine(2)
        cnt+=2
        time.sleep_ms(100)
        lcd.scrolLine(4)
        cnt+=2"""
    time.sleep(2)
    backlight.value(0)
    lcd.fill(0)
    lcd.text("now running on:",0,0,1)
    lcd.text("RaspberryPi pico",0,10,1)
    lcd.show()
    #backlight.value(1)
    time.sleep(1)

