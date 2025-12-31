# themes.py
# This script defines color themes for the Pixela UI application.
from Functions.colorPicker import darker, ideal_text_color
from Functions.getCreds import get_creds

def get_theme():
    creds = get_creds()
    fg = creds.get("accent_color", "#8B5CF6")
    text = ideal_text_color(fg)
    hover = darker(fg, 0.8)
    return fg, hover, text
