# UC1701x-micropython-framebuffer
a simple UC1701x 128*64 dot matrix mono color LCD screen driver written in micropython, using framebuffer.


the main.py is a demo which showing you how to use the class defined in UC1701x.py.


works on raspberry pi pico, may also works on other device that runs micropython.


tested on JLX12864G-1353-BN screen, but it MAY ALSO works on other 128*64 dot matrix mono color LCD screen that driven by UC1701x chip.
you may have to adjust roughContrast,fineContrast,invX,invY parameters to let your UC1701x screen works properly.
if your screen don't have cs/rst pin, don't define them when initialization UC1701x class.


![running effect](https://github.com/ChangboBro/UC1701x-micropython-framebuffer/blob/main/UC1701x%200.jpg?raw=true)

![running effect](https://github.com/ChangboBro/UC1701x-micropython-framebuffer/blob/main/UC1701x%201.jpg?raw=true)
