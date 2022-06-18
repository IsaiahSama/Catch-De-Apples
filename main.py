import arcade
import arcade.color


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.apple = None
        self.apples = None
        self.player = None

        # The Co-ordinates of the player
        self.player_x = None 
        self.player_y = None

        self.setup()

    def setup(self):
        player = ":resources:images/space_shooter/playerShip1_blue.png"

        self.player = arcade.Sprite(player, 1)
        self.player.set_position(self.width // 2, self.height * 0.2)

        self.apple = "./Assets/apple.png"

        self.apples = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()

        self.player.draw()
        self.apples.draw()

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    
    
if __name__ == "__main__":
    GameWindow(1280, 720, "Catch De Apple")
    arcade.run()