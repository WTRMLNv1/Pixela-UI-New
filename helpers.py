# from json import load, dump, JSONDecodeError
from customtkinter import CTkLabel, CTkButton, CTkImage #, CTkFrame, CTk
# from tkinter import messagebox, colorchooser
from PIL import Image

DEFAULT_FONT = ("Cascadia Code", 14)


# ========= WIDGET HELPER FUNCTIONS ========== 
def create_label(master: object, text:str, text_color="white" ,size:int=14,font_family:str="Cascadia Code", image:object=None) -> object:
    """Creates a label with the text, font, color, and image provided on the parent provided

    Args:
        master (object): The parent to put the label on.
        text (str): The text of the Label
        text_color (str, optional): The color of the text. Defaults to "white".
        size (int, optional): The size of the text. Defaults to 14.
        font_family (str, optional): The font of the text. Defaults to "Cascadia Code.
        image (object, optional): The image to add to the text. Defaults to None.

    Returns:
        object: A CTKLabel object
    """
    return CTkLabel(master=master, text=text,text_color=text_color ,image=image, font=(font_family, size))

def add_image(root: object, path:str, size:tuple=(100, 100)) -> object:
    """Creates a CTkLabel with the image whose path is provided of the size provided

    Args:
        root (object): The root CTk object or CTkFrame object to add the label on to
        path (str): The path of the image to add
        size (tuple, optional): The size of the image. Defaults to (100, 100).

    Returns:
        object: A CTkLabel object with the image provided 
    """
    image = CTkImage(dark_image=Image.open(path), size=size)
    return create_label(root, "", image=image)

def add_buttons(master: object, text: str, image_path:str=None, command=None, font_size:int=14, text_color:str="White", font:str="Cascadia Code"):
    """Creates a CTkButton with the specified arguements

    Args:
        master (object): master to put the button on
        text (str): Text to put in the button
        image_path (str, optional): Path of the image. Defaults to None.
        command (_type_, optional): What the button should do when clicked. Defaults to None.
        font_size (int, optional): Size of the font. Defaults to 14.
        text_color (str, optional): Text color. Defaults to "White".
        font (str, optional): Font family. Defaults to "Cascadia Code".
    Returns:
        object: A CTkButton object
    """
    image = CTkImage(dark_image=Image.open(image_path))
    return CTkButton(master=master, text=text, command=command, image=image, font=(font, font_size), text_color=text_color)

def create_title(master: object, text:str):
    """Creates a title label with the text provided

    Args:
        master (object): The parent to put the label on.
        text (str): The text of the Label

    Returns:
        object: A CTKLabel object
    """
    return CTkLabel(master=master, text=text, text_color="white", font=("Cascadia Code", 20, "bold"))


# ========= Testing area ========= #
if __name__ == "__main__":
    None

