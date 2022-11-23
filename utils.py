import mouse
import keyboard

class Cursor:
    def move(x, y, duration=1):
        mouse.move(x, y , absolute=True, duration=duration)

    def left_click():
        mouse.double_click()

    def right_click():
        mouse.right_click()

class Keyboard:
    def write(text):
        keyboard.write(text)
