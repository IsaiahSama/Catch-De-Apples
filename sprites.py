import arcade

import random
import utils


apple_types = {
    "APPLE": {
        'points': 10,
        'source': "./Assets/apple.png"
    },
    "SPECIAL": {
        'points': 15,
        'source': "./Assets/green_apple.png"
    }
}

PLAYER = ":resources:images/space_shooter/playerShip1_blue.png"
CLOUDLINE = "./Assets/cloud_line.png"

class Player(arcade.Sprite):
    """The class to represent the player!
    
    Attrs:
        player_x (int): The x position of the player
        player_y (int): The y position of the player
        speed (int): The speed of the player
        hunger (int): The hunger level of the player
        
    Methods:
        feed(points:int): Increases the player's hunger by the number of points
        move(direction:int, delta_time:float, boosting:bool): Used to move the sprite left or right
        update_position(): Used to update the position of the sprite, then call update()"""

    def __init__(self):
        super().__init__(PLAYER)

        # The window
        self.window = arcade.get_window()

        # The Co-ordinates of the player
        # The center of the screen on the x axis, and near the bottom on the y axis
        self.player_x = self.window.width // 2 
        self.player_y = self.window.height * 0.1
        self.player_speed = 600
        self.hunger = 100
        self.radius = self.width // 2

    def feed(self, points:int) -> None:
        """Method used to increase the player's hunger by a given number of points
        
        Args:
            points (int): The number of points to increase the hunger by."""

        self.hunger += points
        if self.hunger > 100:
            self.hunger = 100

    def move(self, direction:int, delta_time:float, boosting:bool) -> None:
        """Used to move the sprite in a direction.
        
        Args:
            direction (int): The direction. 1 for right, -1 for left.
            delta_time (float): Delta time!
            boosting (bool): Whether the character is boosting or not"""

        change_speed = self.player_speed * delta_time * direction
        if boosting: change_speed *= 1.5
        self.player_x += change_speed

        if self.player_x + (self.radius) > self.window.width: self.player_x = self.window.width - (self.radius)
        if self.player_x - (self.radius) < 0: self.player_x = 0 + (self.radius)

    def update_position(self):
        """Used to update the position of the sprite"""

        self.set_position(self.player_x, self.player_y)
        self.update()

class Apple(arcade.Sprite):
    """An Apple Class template used to represent apples!!!
    
    Attrs:
        points (int): How many points the apple gives
        apple_type(str): The type of apple it is.

    Methods:
        fall(): Used to cause the apple to fall."""

    def __init__(self, filename:str, points:int, apple_type:str):
        super().__init__(filename)
        self.points = points
        self.apple_type = apple_type

    def fall(self) -> None:
        """Used to cause the apple to move downwards."""

        self.center_y -= utils.GRAVITY

        if self.center_y <= 0 + 32:
            self.remove_from_sprite_lists()


def create_apple() -> Apple:
    apple_type = random.choice(list(apple_types.keys()))
    apple_data = apple_types[apple_type]
    points, source = apple_data['points'], apple_data['source']

    apple = Apple(source, points, apple_type)

    window = arcade.get_window()

    apple.set_position(window.width * random.random(), window.height)

    return apple


class CloudLine(arcade.Sprite):
    """Cloud line sprite used to decorate the sky."""

    def __init__(self, filename:str):
        super().__init__(filename, 5)

    def update(self):
        self.center_y -= 20
        if self.center_y <= 0 + 2.5:
            self.remove_from_sprite_lists()

        super().update()

def create_cloud_line() -> CloudLine:
    """Used to create a cloudline."""
    window = arcade.get_window()

    cloud = CloudLine(CLOUDLINE)

    cloud.set_position(random.random() * window.width, window.height)
    return cloud