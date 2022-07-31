"""All other views goes here"""

import arcade, arcade.key
import main, utils

class LevelView(arcade.View):
    """View used to display the level changes to the user
    
    Attrs:
        level - The level to display"""

    def __init__(self, level:int):
        super().__init__()
        self.level = level

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

    def on_draw(self):
        self.clear()

        arcade.draw_text(f"LEVEL {self.level}", self.window.width * 0.5, self.window.height * 0.7, font_size=20)

        arcade.draw_text("PRESS ENTER TO BEGIN", self.window.width * 0.43, self.window.height * 0.6, font_size=13)
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            utils.ViewManager.load_view(main.GameView)