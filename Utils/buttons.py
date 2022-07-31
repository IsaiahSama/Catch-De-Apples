import arcade.gui
import arcade


class Button(arcade.gui.UIFlatButton):
    """Base class for buttons to be used throughout the game
    
    Attrs:
        per_x (float): A percentage value (0.0 - 1.0) for where the button will be placed on the x axis
        per_y (float): A percentage value (0.0 - 1.0) for where the button will be placed on the y axis
        text (str): The text for the button
        callback (Func): The function to call when the button is clicked
        width (float): The width of the button
        height (float): The height of the button"""

    def __init__(self, per_x:float, per_y:float, text:str, callback, width:float=200, height:float=50):
        window = arcade.get_window()
        super().__init__(window.width * per_x, window.height * per_y, width, height, text)
        self.callback = callback

    def on_click(self, event):
        self.callback()