import arcade, arcade.color
from .Utils import buttons


class StartView(arcade.View):
    """Screen which provides the start menu for the game"""

    def __init__(self):
        super().__init__()

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.start_button = buttons.Button("Start Game", self.start_game)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Welcome to Catch De Apples", self.window.width * 0.35, self.window.height * 0.8, font_size=20)


    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    def start_game(self):
        print("Button works!")