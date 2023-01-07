# UC1701x-micropython-framebuffer
a simple UC1701x 128*64 dot matrix mono color LCD screen driver written in micropython, using framebuffer.


the main.py is a demo which showing you how to use the class defined in UC1701x.py.


works on raspberry pi pico, may also works on other device that runs micropython.


tested on JLX12864G-1353-BN screen, but it may also works on other 128*64 dot matrix mono color LCD screen that drived by UC1701x chip.
you may have to adjust roughContrast,fineContrast,invX,invY parameters to let your UC1701x drived screen works properly.
if your screen don't have cs/rst pin, don't define them when initialization UC1701x class.


