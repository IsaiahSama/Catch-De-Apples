import arcade

import random


apple_types = {
    "APPLE": {
        'points': 10,
        'source': "./Assets/apple.png"
    },
    "SPECIAL": {
        'points': 15,
        'source': "./Assets/SpecialApple.png"
    }
}


class Apple(arcade.Sprite):
    """An Apple Class template used to represent apples!!!
    
    Attrs:
        points (int): How many points the apple gives
        apple_type(str): The type of apple it is.

    Methods:
        pass"""

    def __init__(self, filename:str, points:int, apple_type:str):
        super().__init__(filename)
        self.points = points
        self.apple_type = apple_type


def create_apple() -> Apple:
    apple_type = random.choice(list(apple_types.keys()))
    apple_data = apple_types[apple_type]
    points, source = apple_data['points'], apple_data['source']

    apple = Apple(source, points, apple_type)

    window = arcade.get_window()

    apple.set_position(window.width * random.random(), window.height)

    return apple