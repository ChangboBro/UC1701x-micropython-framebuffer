# UC1701x-micropython-framebuffer
a simple UC1701x 128*64 dot matrix mono color LCD screen driver written in micropython, using framebuffer.


the main.py is a demo which showing you how to use the class defined in UC1701x.py.
main.py用来演示怎么使用UC1701x.py中定义的class


works on raspberry pi pico, may also works on other device(mcu) that runs micropython.
能运行在树莓派pico上，别的运行micropython的设备(mcu)也许也能运行


tested on JLX12864G-1353-BN screen, but it MAY ALSO works on other 128*64 dot matrix mono color LCD screen that driven by UC1701x chip.
you may have to adjust roughContrast,fineContrast,invX,invY parameters to let your UC1701x screen works properly.
if your screen don't have cs/rst pin, don't define them when initialization UC1701x class.
用JLX12864G-1353-BN这个屏幕测试的，别的被UC1701x驱动的单色点阵LCD屏幕应该也能适配。
如果你用的屏幕和我测试的不一样，你可以试试调整实例化的时候使用的roughContrast,fineContrast,invX,invY参数来让你的屏幕能正常工作。
如果你的屏幕没有cs/rst引脚，实例化的时候不要定义这两个引脚就行了。


![running effect0](https://github.com/ChangboBro/UC1701x-micropython-framebuffer/blob/main/UC1701x%200.jpg?raw=true)

![running effect1](https://github.com/ChangboBro/UC1701x-micropython-framebuffer/blob/main/UC1701x%201.jpg?raw=true)
