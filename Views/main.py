import arcade
import arcade.color
import arcade.key

from .Utils import utils, sprites
import random

class MainView(arcade.View):
    def __init__(self, width, height, title):
        super().__init__()

        self.apples = None
        self.cloud_lines = None
        self.player = None

        self.points = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.moving_left = False
        self.moving_right = False
        self.boosting = False
        self.game_over = False
        self.started = False

        self.timer = utils.Timer()

        self.moosic = arcade.load_sound(utils.MAIN_SONG, True)
        self.apple_sound = arcade.load_sound(utils.APPLE_SOUND)
        self.game_end_sound = arcade.load_sound(utils.GAME_OVER_SOUND)

        self.setup()

    def setup(self):

        self.player = sprites.Player()
        self.player.update_position()

        self.apples = arcade.SpriteList(use_spatial_hash=True)
        self.cloud_lines = arcade.SpriteList()


    def on_draw(self):
        arcade.start_render()

        if not self.started:
            arcade.Text("Press Enter to begin your journey!", self.width * 0.35, self.height * 0.5, font_size=20).draw()
        elif not self.game_over and self.started:
            self.player.draw()
            self.apples.draw()
            self.cloud_lines.draw()

            arcade.Text(f"Your score is {self.points}", 30, self.height * 0.95).draw()
            arcade.Text(f"Hunger: {self.player.hunger}", 30, self.height * 0.8).draw()
            if self.boosting:
                arcade.Text("BOOSTING!!! (Draining hunger in exchange for speed)", self.width * 0.4, self.height * 0.1, color=arcade.color.RED).draw()
        else:
            self.apples.clear()
            arcade.Text(f"You lose!. Your final score: {self.points}", self.width // 4, self.height // 2, font_size=30).draw()


    def on_update(self, delta_time: float):
        if not self.started: return
        if self.game_over: return
        if self.timer.timer_finished(id(self.apples)):
            self.apples.append(sprites.create_apple())
            self.timer.start_timer(id(self.apples), 2)

        if self.timer.timer_finished(id(self.cloud_lines)):
            self.cloud_lines.append(sprites.create_cloud_line())
            self.timer.start_timer(id(self.cloud_lines), random.random())

        player_collision_list = arcade.check_for_collision_with_list(self.player, self.apples)

        if player_collision_list:
            for apple in player_collision_list:
                self.points += apple.points
                self.player.feed(apple.points)
                arcade.play_sound(self.apple_sound)
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
            arcade.play_sound(self.game_end_sound)

        if self.moving_right: self.player.move(1, delta_time, self.boosting)
        if self.moving_left: self.player.move(-1, delta_time, self.boosting)

        self.player.update_position()
        self.apples.update()
        self.cloud_lines.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = True
        if symbol == arcade.key.LEFT: self.moving_left = True
        if symbol == arcade.key.Z: self.boosting = not self.boosting
        if not self.started and symbol == arcade.key.ENTER: 
            self.started = True
            arcade.play_sound(self.moosic, looping=True, volume=0.7)
        if symbol == arcade.key.ESCAPE: arcade.exit()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = False
        if symbol == arcade.key.LEFT: self.moving_left = False

