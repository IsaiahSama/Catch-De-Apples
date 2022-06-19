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

        self.points = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.moving_left = False
        self.moving_right = False
        self.boosting = False
        self.game_over = False
        self.started = False

        self.timer = utils.Timer()

        self.setup()

    def setup(self):

        self.player = sprites.Player()
        self.player.update_position()

        self.apples = arcade.SpriteList(use_spatial_hash=True)


    def on_draw(self):
        arcade.start_render()

        if not self.started:
            arcade.Text("Press Enter to begin your journey!", self.width * 0.35, self.height * 0.5, font_size=20).draw()
        elif not self.game_over and self.started:
            self.player.draw()
            self.apples.draw()

            arcade.Text(f"Your score is {self.points}", 30, self.height * 0.95).draw()
            arcade.Text(f"Hunger: {self.player.hunger}", 30, self.height * 0.8).draw()
            if self.boosting:
                arcade.Text("BOOSTING!!! (Draining hunger in exchange for speed)", self.width * 0.4, self.height * 0.1, color=arcade.color.RED).draw()
        else:
            self.apples.clear()
            arcade.Text(f"You lose!. Your final score: {self.points}", self.width // 4, self.height // 2, font_size=30).draw()


    def on_update(self, delta_time: float):
        if not self.started: return
        if self.timer.timer_finished(id(self.apples)):
            self.apples.append(sprites.create_apple())
            self.timer.start_timer(id(self.apples), 2) 

        player_collision_list = arcade.check_for_collision_with_list(self.player, self.apples)

        if player_collision_list:
            for apple in player_collision_list:
                self.points += apple.points
                self.player.feed(apple.points)
                apple.remove_from_sprite_lists()

        for apple in self.apples:
            apple.fall()

        if self.timer.timer_finished(id(self.player.hunger)):
            self.player.feed(-5)
            self.timer.start_timer(id(self.player.hunger), 1)

        if self.boosting:
            if self.timer.timer_finished(id(self.boosting)):
                self.player.feed(-1)
                self.timer.start_timer(id(self.boosting), 0.7)

        if self.player.hunger <= 0:
            self.game_over = True

        if self.moving_right: self.player.move(1, delta_time, self.boosting)
        if self.moving_left: self.player.move(-1, delta_time, self.boosting)

        self.player.update_position()
        self.apples.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = True
        if symbol == arcade.key.LEFT: self.moving_left = True
        if symbol == arcade.key.Z: self.boosting = not self.boosting
        if not self.started and symbol == arcade.key.ENTER: self.started = True
        if symbol == arcade.key.ESCAPE: arcade.exit()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = False
        if symbol == arcade.key.LEFT: self.moving_left = False

    
    
if __name__ == "__main__":
    GameWindow(1280, 720, "Catch De Apple")
    arcade.run()