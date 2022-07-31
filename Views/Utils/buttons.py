import arcade.gui
import arcade


class Button(arcade.gui.UIFlatButton):
    """Base class for buttons to be used throughout the game
    
    Attrs:
        text (str): The text for the button
        callback (Func): The function to call when the button is clicked
        per_x (float): A percentage value (0.0 - 1.0) for where the button will be placed on the x axis
        per_y (float): A percentage value (0.0 - 1.0) for where the button will be placed on the y axis
        width (float): The width of the button
        height (float): The height of the button"""

    def __init__(self, text:str, callback, per_x:float=0.5, per_y:float=0.5, width:float=200, height:float=50):
        window = arcade.get_window()
        super().__init__(window.width * per_x, window.height * per_y, width, height, text)
        self.callback = callback

    def on_click(self, event):
        self.callback()