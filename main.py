import utils


def main():
    utils.Cursor.move(20, 100)
    utils.Cursor.move(700, 300)
    utils.Cursor.left_click()
    utils.Keyboard.write("HELLO")
    utils.Cursor.move(1000, 100)
    utils.Cursor.right_click()

if __name__ == '__main__':
    main()