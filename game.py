import arcade
from Views.start import StartView


SCREEN_WIDTH, SCREEN_HEIGHT, TITLE = 1000, 650, "Catch De Apples"


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = StartView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()