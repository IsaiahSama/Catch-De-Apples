import arcade
import arcade.color
import arcade.key

import utils, sprites, views
import random

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fruits = None
        self.cloud_lines = None
        self.player = None
        self.timer = utils.Timer()

        self.game_state = utils.SaveStateManager.load_state()
        self.level = self.game_state["LEVEL"]
        self.points = self.game_state["POINTS"]
        self.level_info = utils.get_level_info(self.level)

        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.moving_left = False
        self.moving_right = False
        self.boosting = False
        self.game_over = False


        # self.moosic = arcade.load_sound(utils.MAIN_SONG, True)
        self.game_end_sound = arcade.load_sound(utils.GAME_OVER_SOUND)

        self.moosic = utils.MAIN_SONG


    def setup(self):
        utils.SoundManager.start_playing(self.moosic, True, 0.7, True)
        # arcade.play_sound(self.moosic, looping=True, volume=0.7)

        self.player = sprites.Player()
        self.player.update_position()

        self.fruits = arcade.SpriteList()
        self.cloud_lines = arcade.SpriteList()

        fruit_info = utils.load_yaml("stageinfo")["Fruits"]

        self.fruit_objs = [sprites.Fruit(fruit_info[fruit]) for fruit in self.level_info["FRUITS"]]
        
        for obj in self.fruit_objs:
            self.timer.start_timer(id(obj), obj.frequency)


    def on_draw(self):
        arcade.start_render()

        if not self.game_over:
            self.player.draw()
            self.fruits.draw()
            self.cloud_lines.draw()

            arcade.Text(f"Your score is {self.points}/{self.level_info['GOAL']}", 30, self.window.height * 0.95).draw()
            arcade.Text(f"Hunger: {self.player.hunger}", 30, self.window.height * 0.8).draw()
            if self.boosting:
                arcade.Text("BOOSTING!!! (Draining hunger in exchange for speed)", self.window.width * 0.4, self.window.height * 0.1, color=arcade.color.RED).draw()
        else:
            self.fruits.clear()
            arcade.Text(f"You lose!. Your final score: {self.points}", self.window.width // 4, self.window.height // 2, font_size=30).draw()


    def on_update(self, delta_time: float):
        if self.game_over:
            utils.SoundManager.stop_playing(self.moosic)
            self.save_game()
            utils.ViewManager.load_view(views.GameOverView)

        if self.points >= self.level_info["GOAL"]:
            self.level += 1
            self.save_game()
            utils.ViewManager.load_view(views.LevelView, level=self.level)

        for fruit in self.fruit_objs:
            if self.timer.timer_finished(id(fruit)):
                self.fruits.append(sprites.create_fruit(fruit.name))
                self.timer.start_timer(id(fruit), fruit.frequency)

        # if self.timer.timer_finished(id(self.fruits)):
        #     self.fruits.append(sprites.create_fruit(self.level_info["FRUITS"]))
        #     self.timer.start_timer(id(self.fruits), 2)

        if self.timer.timer_finished(id(self.cloud_lines)):
            self.cloud_lines.append(sprites.create_cloud_line())
            self.timer.start_timer(id(self.cloud_lines), random.random())

        player_collision_list = arcade.check_for_collision_with_list(self.player, self.fruits)

        if player_collision_list:
            for fruit in player_collision_list:
                self.points += fruit.points
                self.player.feed(fruit.points)
                arcade.play_sound(fruit.sound)
                fruit.remove_from_sprite_lists()

        for fruit in self.fruits:
            fruit.fall()

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
        self.fruits.update()
        self.cloud_lines.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = True
        if symbol == arcade.key.LEFT: self.moving_left = True
        if symbol == arcade.key.Z: self.boosting = not self.boosting
        if symbol == arcade.key.ESCAPE: arcade.exit()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.RIGHT: self.moving_right = False
        if symbol == arcade.key.LEFT: self.moving_left = False

    def save_game(self):
        """Method used to save the current game state."""

        self.game_state = utils.SaveStateManager.update_state(self.game_state, level=self.level, points=self.points)
        utils.SaveStateManager.save_state(self.game_state)
