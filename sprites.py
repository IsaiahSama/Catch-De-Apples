import arcade


class Apple(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename)

    def on_update(self, delta_time: float = 1 / 60):
        return super().on_update(delta_time)