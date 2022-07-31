import arcade, arcade.color, arcade.gui
import buttons
from main import GameView


class StartView(arcade.View):
    """Screen which provides the start menu for the game"""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

    def setup(self):
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.v_box.add(buttons.Button("Start Game", self.start_game))

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

    def start_game(self):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)