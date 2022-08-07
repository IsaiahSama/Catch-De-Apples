"""All other views goes here"""

import arcade, arcade.key, arcade.gui
import main, utils, buttons, start

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

        arcade.draw_text("PRESS ENTER TO BEGIN", self.window.width * 0.45, self.window.height * 0.6, font_size=13)
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            utils.ViewManager.load_view(main.GameView)

class GameOverView(arcade.View):
    """View used to display the game over screen."""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

    def setup(self):
        self.h_box.add(buttons.Button("TRY AGAIN", self.try_again, 0.3, 0.4).with_space_around(right=20))

        self.h_box.add(buttons.Button("RETURN TO MENU", self.main_menu))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.h_box
            )
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text("GAME OVER!!!", self.window.width *0.4, self.window.height *0.8, arcade.color.RED, 25)
        
        self.manager.draw()

    def try_again(self):
        utils.ViewManager.load_view(main.GameView)
    
    def main_menu(self):
        utils.ViewManager.load_view(start.StartView)