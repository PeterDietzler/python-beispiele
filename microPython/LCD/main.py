#
# https://techtotinker.blogspot.com/2021/01/008-micropython-technotes-16x2-lcd.html
#


'''
from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x20

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

# The following line of code should be tested
# using the REPL:

# 1. To print a string to the LCD:
#    lcd.putstr('Hello world')
# 2. To clear the display:
#	 lcd.clear()
# 3. To control the cursor position:
# 	 lcd.move_to(2, 1)
# 4. To show the cursor:
#  	 lcd.show_cursor()
# 5. To hide the cursor:
#	 lcd.hide_cursor()
# 6. To set the cursor to blink:
#	 lcd.blink_cursor_on()
# 7. To stop the cursor on blinking:
#	 lcd.blink_cursor_off()
# 8. To hide the currently displayed character:
#	 lcd.display_off()
# 9. To show the currently hidden character:
#	 lcd.display_on()
# 10. To turn off the backlight:
#	 lcd.backlight_off()
# 11. To turn ON the backlight:
#	 lcd.backlight_on()
# 12. To print a single character:
#	 lcd.putchar('x')
# 13. To print a custom character:
#	 happy_face = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x11, 0x0E, 0x00])
#	 lcd.custom_char(0, happy_face)
#	 lcd.putchar(chr(0))
'''

#'''
from time import sleep_ms, ticks_ms 
from machine import I2C, Pin 
from i2c_lcd import I2cLcd 

DEFAULT_I2C_ADDR = 0x20

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

lcd.clear()
lcd.putstr('Example # 2')
sleep_ms(1000)
count = 0

while True:
    print('Counter: {}'.format(count))
    lcd.clear() # Clears the LCD,
                # Sets the cursor position to 0,0 
    lcd.putstr('Counter: {}' .format(count))
    count = count + 1
    sleep_ms(1000)

#'''


