import arcade
import arcade.color
import arcade.key

import utils
import sprites
import random

from random import random


class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.apples = None
        self.player = None
        self.hunger = 0

        self.points = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

        # The Co-ordinates of the player
        # The center of the screen on the x axis, and near the bottom on the y axis
        self.player_x = self.width // 2 
        self.player_y = self.height * 0.2
        self.player_speed = 600

        self.moving_left = False
        self.moving_right = False
        self.boosting = False
        self.game_over = False
        self.started = False

        self.timer = utils.Timer()

        self.setup()

    def setup(self):
        player = ":resources:images/space_shooter/playerShip1_blue.png"

        self.player = arcade.Sprite(player, 1)
        self.player.set_position(self.player_x, self.player_y)
        self.hunger = 100

        self.apple = "./Assets/apple.png"
        self.special_apple = "./Assets/SpecialApple.png"

        self.apples = arcade.SpriteList(use_spatial_hash=True)


    def on_draw(self):
        arcade.start_render()

        if not self.started:
            arcade.Text("Press Enter to begin your journey!", self.width * 0.35, self.height * 0.5, font_size=20).draw()
        elif not self.game_over and self.started:
            self.player.draw()
            self.apples.draw()

            arcade.Text(f"Your score is {self.points}", 30, self.height * 0.95).draw()
            arcade.Text(f"Hunger: {self.hunger}", 30, self.height * 0.8).draw()
            if self.boosting:
                arcade.Text("BOOSTING!!! (Draining hunger in exchange for speed)", self.width * 0.4, self.height * 0.1, color=arcade.color.RED).draw()
        else:
            self.apples.clear()
            arcade.Text(f"You lose!. Your final score: {self.points}", self.width // 4, self.height // 2, font_size=30).draw()


    def on_update(self, delta_time: float):
        if not self.started: return
        if self.timer.timer_finished(id(self.apples)):
            self.apples.append(sprites.create_apple())
            self.timer.start_timer(id(self.apples), 3) 

        player_collision_list = arcade.check_for_collision_with_list(self.player, self.apples)

        if player_collision_list:
            for apple in player_collision_list:
                self.points += apple.points
                self.hunger += apple.points
                apple.remove_from_sprite_lists()

        for apple in self.apples:
            apple.center_y -= utils.GRAVITY

            if apple.center_y <= 0 + 32:
                apple.remove_from_sprite_lists()

        if self.timer.timer_finished(id(self.hunger)):
            self.hunger -= 5
            self.timer.start_timer(id(self.hunger), 1)

        if self.boosting:
            if self.timer.timer_finished(id(self.boosting)):
                self.hunger -= 1
                self.timer.start_timer(id(self.boosting), 0.7)

        if self.hunger > 100:
            self.hunger = 100
        if self.hunger <= 0:
            self.game_over = True


        if self.moving_right: self.player_x += self.player_speed * delta_time if not self.boosting else self.player_speed * 1.5 * delta_time
        if self.moving_left: self.player_x -= self.player_speed * delta_time if not self.boosting else self.player_speed * 1.5 * delta_time

        self.player.set_position(self.player_x, self.player_y)
        self.player.update()
        self.apples.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = True
        if symbol == arcade.key.LEFT: self.moving_left = True
        if symbol == arcade.key.Z: self.boosting = not self.boosting
        if not self.started and symbol == arcade.key.ENTER:
            self.started = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = False
        if symbol == arcade.key.LEFT: self.moving_left = False

    
    
if __name__ == "__main__":
    GameWindow(1280, 720, "Catch De Apple")
    arcade.run()