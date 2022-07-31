import arcade, arcade.color, arcade.gui
import buttons
import utils

import views


class StartView(arcade.View):
    """Screen which provides the start menu for the game"""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.v_box.add(buttons.Button("New Game", self.new_game).with_space_around(bottom=20))

        if utils.SaveStateManager.load_state() != utils.default_state:
            self.v_box.add(buttons.Button("Load Game", self.start_game).with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center_x',
                anchor_y='center_y',
                child=self.v_box
            )
        )

    def on_draw(self):
        self.clear()

        arcade.draw_text("Welcome to Catch De Apples", self.window.width * 0.32, self.window.height * 0.8, font_size=20)

        self.manager.draw()

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    def new_game(self):
        """Used to start a new game"""
        utils.SaveStateManager.save_state(utils.default_state)
        self.start_game()

    def start_game(self):
        """Used to start the game!"""
        utils.ViewManager.load_view(views.LevelView, level=utils.SaveStateManager.load_state()['LEVEL'])