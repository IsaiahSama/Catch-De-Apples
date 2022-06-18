import arcade
import arcade.color
import arcade.key


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.apple = None
        self.apples = None
        self.player = None


        arcade.set_background_color(arcade.color.SKY_BLUE)

        # The Co-ordinates of the player
        # The center of the screen on the x axis, and near the bottom on the y axis
        self.player_x = self.width // 2 
        self.player_y = self.height * 0.2
        self.player_speed = 500

        self.moving_left = False
        self.moving_right = False

        self.setup()

    def setup(self):
        player = ":resources:images/space_shooter/playerShip1_blue.png"

        self.player = arcade.Sprite(player, 1)
        self.player.set_position(self.player_x, self.player_y)


        self.apple = "./Assets/apple.png"

        self.apples = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()

        self.player.draw()

        self.apples.draw()

    def on_update(self, delta_time: float):
        if self.moving_right: self.player_x += self.player_speed * delta_time
        if self.moving_left: self.player_x -= self.player_speed * delta_time

        self.player.set_position(self.player_x, self.player_y)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = True
        if symbol == arcade.key.LEFT: self.moving_left = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = False
        if symbol == arcade.key.LEFT: self.moving_left = False

    
    
if __name__ == "__main__":
    GameWindow(1280, 720, "Catch De Apple")
    arcade.run()