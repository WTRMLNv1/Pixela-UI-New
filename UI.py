# UI.py
import os
import customtkinter as ctk
from Functions import core
from tkinter import messagebox, colorchooser, CENTER, W
from PIL import Image
from datetime import datetime
from Save_chart import save_chart
import threading
from Functions.themes import get_theme
# Optional imports from your project
try:
    from Functions.getCreds import get_creds, update_creds
    from Functions import getDate
    from Functions.colorPicker import hex_to_hsv, hsv_to_hex, darker
except Exception:
    get_creds = None
    getDate = None
    hex_to_hsv = None
    hsv_to_hex = None
    darker = None

# Fallback create_title if helpers not found
try:
    from helpers import *
except Exception:
    def create_title(master, text=""):
        return ctk.CTkLabel(master, text=text, font=("Helvetica", 20, "bold"))


class UI:
    def __init__(self):
        # === Setup === #
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Pixela")
        self.root.minsize(500, 600)
        self.root.resizable(False, False)

        # Try to set icon safely
        try:
            ico_path = os.path.join("assets", "pixela-icon-no-text_ico.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except Exception:
            pass

        # Content frame (full screen, swappable area)
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.content_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.9, relheight=0.9)

        # Default screen
        self.show_screen("home")

        self.root.mainloop()

    def show_screen(self, screen_name: str):
        # Clear content frame only
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if screen_name == "home":
            HomeScreen(self)
        elif screen_name == "settings":
            SettingsScreen(self)
        elif screen_name == "signup":
            SignUpScreen(self)
        elif screen_name == "login":
            LoginScreen(self)
        elif screen_name == "add_pixel":
            AddPixelScreen(self)
        elif screen_name == "create_graph":
            CreateGraphScreen(self)
        else:
            ctk.CTkLabel(
                self.content_frame, text=f"Unknown screen: {screen_name}"
            ).place(relx=0.5, rely=0.5, anchor="center")


# =================== HomeScreen =================== #
class HomeScreen:
    def __init__(self, ui):
        threading.Thread(target=save_chart, daemon=True).start()
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.fg, self.hover, self.text = get_theme()
        self.add_widgets()
        # save_chart()

    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Home", 
                                  font=ctk.CTkFont(size=20, family="Cascadia Code"), 
                                  text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)

        divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider.place(relx=0.5, rely=0.1, anchor=CENTER)

        # Heatmap
        self.heatmap_img = ctk.CTkImage(dark_image=Image.open("assets/heatmap.png"), size=(400, 140))
        self.heatmap_frame = ctk.CTkFrame(self.ui.content_frame, height=180, width=430, fg_color="#242424")
        self.heatmap_frame.place(relx=0.5, rely=0.30, anchor=CENTER)

        self.img = ctk.CTkLabel(self.heatmap_frame, image=self.heatmap_img, text="")
        self.img.place(x=15, y=10)

        self.heatmap_text = ctk.CTkLabel(self.heatmap_frame, text="Today: 0 minutes", text_color="white", font=ctk.CTkFont(size=10, family="Cascadia Code"), fg_color="transparent")
        self.heatmap_text.place(relx=0.5, y=165, anchor=CENTER)

        # Buttons
        self.login_button = ctk.CTkButton(self.ui.content_frame, text="Login/Sign up", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("login"))
        self.login_button.place(relx=0.05, rely=0.55, relwidth=0.3)
        self.addPixel_button = ctk.CTkButton(self.ui.content_frame, text="Add Pixel", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("add_pixel"))
        self.addPixel_button.place(relx=0.05, rely=0.65, relwidth=0.3)
        self.settings_button = ctk.CTkButton(self.ui.content_frame, text="Settings", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("settings"))
        self.settings_button.place(relx=0.95, rely=0.65, relwidth=0.3, anchor="ne")
        self.createGraph_button = ctk.CTkButton(self.ui.content_frame, text="Create Graph", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("create_graph"))
        self.createGraph_button.place(relx=0.05, rely=0.75, relwidth=0.3)

        # Username display
        try:
            creds = get_creds()
            username = creds.get("username", "Username not found")
        except Exception:
            username = "Username not found"
        self.username_frame = ctk.CTkFrame(self.ui.content_frame, height=40, fg_color="#242424")
        self.username_frame.place(relx=0.97, rely=0.54, anchor="ne", relwidth=0.6)
        self.username_label = ctk.CTkLabel(self.username_frame, text=f"User: {username}", font=self.font14, text_color="white", fg_color="transparent")
        self.username_label.place(relx=0.5, rely=0.5, anchor=CENTER)

# =================== CreateGraphScreen =================== #
class CreateGraphScreen:
    def __init__(self, ui):
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.fg, self.hover, self.text = get_theme()
        self.home_img = ctk.CTkImage(dark_image=Image.open("assets/homebutton.png"))
        self.add_widgets()


    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Create Graph", font=ctk.CTkFont(size=20, family="Cascadia Code"), text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)

        divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.home_button = ctk.CTkButton(self.ui.content_frame, image=self.home_img, text="", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color=self.fg, hover_color=self.hover, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("home"))
        self.home_button.place(relx=0.05, rely=0.05, anchor="w", relwidth=0.1)

        self.graph_name_label = ctk.CTkLabel(self.ui.content_frame, text="Graph Name:", font=self.font14, text_color="white")
        self.graph_name_label.place(relx=0.05, rely=0.15, anchor="w")

        self.graph_name_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter graph name", font=self.font14)  
        self.graph_name_entry.place(relx=0.05, rely=0.2, anchor="w", relwidth=0.8)

        self.graph_unit_label = ctk.CTkLabel(self.ui.content_frame, text="Unit (e.g., minutes):", font=self.font14, text_color="white")
        self.graph_unit_label.place(relx=0.05, rely=0.3, anchor="w")

        self.graph_unit_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter graph unit", font=self.font14)
        self.graph_unit_entry.place(relx=0.05, rely=0.35, anchor="w", relwidth=0.8)

        self.graph_type_label = ctk.CTkLabel(self.ui.content_frame, text="Type (int/float):", font=self.font14, text_color="white")
        self.graph_type_label.place(relx=0.05, rely=0.45, anchor="w")

        self.graph_type_choice = ctk.CTkOptionMenu(self.ui.content_frame, values=["int", "float"], font=self.font14, fg_color="#343638", button_color="#565B5E", button_hover_color="#393A3B", dropdown_fg_color="#393939", dropdown_hover_color="#787878", text_color="white")
        self.graph_type_choice.place(relx=0.05, rely=0.5, anchor="w", relwidth=0.8)

        self.chooser_label = ctk.CTkLabel(self.ui.content_frame, text="Color:", font=self.font14, text_color="white")
        self.chooser_label.place(relx=0.05, rely=0.6, anchor="w")

        self.color_choice = ctk.CTkOptionMenu(self.ui.content_frame, values=["shibafu", "momiji", "sora", "ichou", "ajisai", "kuro"], font=self.font14, fg_color="#343638", button_color="#565B5E", button_hover_color="#393A3B", dropdown_fg_color="#393939", dropdown_hover_color="#787878", text_color="white")
        self.color_choice.place(relx=0.05, rely=0.65, anchor="w", relwidth=0.8)

        self.submit_button = ctk.CTkButton(self.ui.content_frame, text="Create Graph", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.submit_graph)
        self.submit_button.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.3)

    def submit_graph(self):
        name = self.graph_name_entry.get()
        unit = self.graph_unit_entry.get()
        type_ = self.graph_type_choice.get()
        color = self.color_choice.get()
        if not name or not unit or not type_:
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            creds = get_creds()
            username = creds.get("username")
            token = creds.get("tokenID")
            graph_id = name.lower().replace(" ", "_")
            response = core.create_graph(graph_id, name, unit, type_, color, "UTC", token, username)
            if response.get("isSuccess"):
                messagebox.showinfo("Success", "Graph created successfully")
                self.ui.show_screen("home")
            else:
                messagebox.showerror("Error", response.get("message", "Failed to create graph"))
        except Exception as e:
            messagebox.showerror("Error", str(e))
# =================== SignUpScreen =================== #
class SignUpScreen:
    def __init__(self, ui):
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.fg, self.hover, self.text = get_theme()
        self.eye_open_img = ctk.CTkImage(dark_image=Image.open("assets/eye_open.png"), size=(20, 20))
        self.eye_closed_img = ctk.CTkImage(dark_image=Image.open("assets/eye_closed.png"), size=(20, 20))
        self.home_img = ctk.CTkImage(dark_image=Image.open("assets/homebutton.png"))
        self.gray = self.ui.content_frame.cget("fg_color")
        self.add_widgets()

    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold", family="Cascadia Code"), text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)
        
        divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.home_button = ctk.CTkButton(self.ui.content_frame, image=self.home_img, text="", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color=self.fg, hover_color=self.hover, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("home"))
        self.home_button.place(relx=0.05, rely=0.05, anchor="w", relwidth=0.1)
        
        self.username_label = ctk.CTkLabel(self.ui.content_frame, text="Username:", font=self.font14, text_color="white")
        self.username_label.place(relx=0.05, rely=0.15, anchor="w")
        
        self.username_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter your username", font=self.font14)
        self.username_entry.place(relx=0.05, rely=0.2, anchor="w", relwidth=0.8)
        
        self.password_label = ctk.CTkLabel(self.ui.content_frame, text="Password:", font=self.font14, text_color="white")
        self.password_label.place(relx=0.05, rely=0.30, anchor="w")
        
        self.password_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter your password", font=self.font14, show="*")
        self.password_entry.place(relx=0.05, rely=0.35, anchor="w", relwidth=0.8)
        
        self.confirm_password_label = ctk.CTkLabel(self.ui.content_frame, text="Confirm Password:", font=self.font14, text_color="white")
        self.confirm_password_label.place(relx=0.05, rely=0.45, anchor="w")
        
        self.confirm_password_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Re-enter your password", font=self.font14, show="*")
        self.confirm_password_entry.place(relx=0.05, rely=0.5, anchor="w", relwidth=0.8)
        
        self.hide_button = ctk.CTkButton(self.ui.content_frame, image=self.eye_closed_img, text="", width=30, height=30, fg_color=self.fg, hover_color=self.hover, cursor="hand2", command=self.toggle_password)
        self.hide_button.place(relx=0.86, rely=0.35, anchor="w")
        
        self.signup_button = ctk.CTkButton(self.ui.content_frame, text="Sign up", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.sign_up)
        self.signup_button.place(relx=0.5, rely=0.6, anchor=CENTER, relwidth=0.3)
        
        divider2 = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider2.place(relx=0.5, rely=0.65, anchor=CENTER, relwidth=1)
        
        self.login_button = ctk.CTkButton(self.ui.content_frame, text="Login!", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color="#2B2B2B", hover_color="#2B2B2B", text_color="#8B5CF6", cursor="hand2", command=lambda: self.ui.show_screen("login"))
        self.login_button.place(relx=0.38, rely=0.726, anchor=CENTER)
        
        self.login_label = ctk.CTkLabel(self.ui.content_frame, text="Have an account?", font=ctk.CTkFont(size=12, family="Cascadia Code"), text_color="white")
        self.login_label.place(relx=0.05, rely=0.7)

    def toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.configure(show="*")
            self.confirm_password_entry.configure(show="*")
            self.hide_button.configure(image=self.eye_closed_img)
        else:
            self.password_entry.configure(show="")
            self.confirm_password_entry.configure(show="")
            self.hide_button.configure(image=self.eye_open_img)
        self.hide_button.place(relx=0.86, rely=0.35, anchor="w")

    def sign_up(self):
        username = self.username_entry.get()
        token = self.password_entry.get()
        confirm = self.confirm_password_entry.get()
        if token != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        if not username or not token:
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            response = core.create_user(token, username)
            if response.get("isSuccess"):
                update_creds(username=username, tokenID=token)
                messagebox.showinfo("Success", "Account created successfully")
                self.ui.show_screen("home")
            else:
                messagebox.showerror("Error", response.get("message", "Failed to create account"))
        except Exception as e:
            messagebox.showerror("Error", str(e))


# =================== LoginScreen =================== #
class LoginScreen:
    def __init__(self, ui):
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.fg, self.hover, self.text = get_theme()
        self.eye_open_img = ctk.CTkImage(dark_image=Image.open("assets/eye_open.png"), size=(20, 20))
        self.eye_closed_img = ctk.CTkImage(dark_image=Image.open("assets/eye_closed.png"), size=(20, 20))
        self.home_img = ctk.CTkImage(dark_image=Image.open("assets/homebutton.png"))
        self.gray = self.ui.content_frame.cget("fg_color")
        self.add_widgets()

    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Login", font=ctk.CTkFont(size=20, weight="bold", family="Cascadia Code"), text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)
        
        divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.username_label = ctk.CTkLabel(self.ui.content_frame, text="Username:", font=self.font14, text_color="white")
        self.username_label.place(relx=0.05, rely=0.15, anchor="w")
        
        self.username_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter your username", font=self.font14)
        self.username_entry.place(relx=0.05, rely=0.2, anchor="w", relwidth=0.8)
        
        self.password_label = ctk.CTkLabel(self.ui.content_frame, text="Password:", font=self.font14, text_color="white")
        self.password_label.place(relx=0.05, rely=0.30, anchor="w")
        
        self.password_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter your password", font=self.font14, show="*")
        self.password_entry.place(relx=0.05, rely=0.35, anchor="w", relwidth=0.8)
        
        self.hide_button = ctk.CTkButton(self.ui.content_frame, image=self.eye_closed_img, text="", width=30, height=30, fg_color=self.fg, hover_color=self.hover, cursor="hand2", command=self.toggle_password)
        self.hide_button.place(relx=0.86, rely=0.35, anchor="w")
        
        self.login_button = ctk.CTkButton(self.ui.content_frame, text="Login", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.login)
        self.login_button.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.3)
        
        divider2 = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider2.place(relx=0.5, rely=0.55, anchor=CENTER, relwidth=1)
        
        self.signup_button = ctk.CTkButton(self.ui.content_frame, text="Sign Up!", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color="#2B2B2B", hover_color="#2B2B2B", text_color="#8B5CF6", cursor="hand2", command=lambda: self.ui.show_screen("signup"))
        self.signup_button.place(relx=0.5, rely=0.626, anchor=CENTER)
        
        self.name_label = ctk.CTkLabel(self.ui.content_frame, text="Don't have an account?", font=ctk.CTkFont(size=12, family="Cascadia Code"), text_color="white")
        self.name_label.place(relx=0.05, rely=0.6)
        
        self.home_button = ctk.CTkButton(self.ui.content_frame, image=self.home_img, text="", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color=self.fg, hover_color=self.hover, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("home"))
        self.home_button.place(relx=0.05, rely=0.05, anchor="w", relwidth=0.1)

    def toggle_password(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.configure(show="*")
            self.hide_button.configure(image=self.eye_closed_img)
        else:
            self.password_entry.configure(show="")
            self.hide_button.configure(image=self.eye_open_img)
        self.hide_button.place(relx=0.86, rely=0.35, anchor="w")

    def login(self):
        username = self.username_entry.get()
        token = self.password_entry.get()
        if not username or not token:
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            # For login, just update creds, since Pixela doesn't have login
            update_creds(username=username, tokenID=token)
            messagebox.showinfo("Success", "Logged in successfully")
            self.ui.show_screen("home")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# =================== AddPixelScreen =================== #
class AddPixelScreen:
    def __init__(self, ui):
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.font20 = ctk.CTkFont(size=20, family="Cascadia Code", weight="bold")
        self.fg, self.hover, self.text = get_theme()
        self.home_img = ctk.CTkImage(dark_image=Image.open("assets/homebutton.png"))
        try:
            creds = get_creds() or {}
        except Exception:
            creds = {}
        self.creds = creds
        graphs_val = creds.get('graphID', [])
        if isinstance(graphs_val, list):
            self.graphs = graphs_val if graphs_val else ["No Graphs Found"]
        else:
            # single graph id stored as string
            self.graphs = [graphs_val] if graphs_val else ["No Graphs Found"]
        self.hasGraphs = bool(self.graphs and self.graphs[0] != "No Graphs Found")
        self.add_widgets()
        
    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Add Pixel", font=self.font20, text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)
        
        self.divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        self.divider.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.home_button = ctk.CTkButton(self.ui.content_frame, image=self.home_img, text="", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color=self.fg, hover_color=self.hover, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("home"))
        self.home_button.place(relx=0.05, rely=0.05, anchor="w", relwidth=0.1)
        
        self.date_label = ctk.CTkLabel(self.ui.content_frame, text="Date (YYYYMMDD):", font=self.font14, text_color="white")
        self.date_label.place(relx=0.05, rely=0.15)
        
        self.date_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter the date", font=self.font14)
        self.date_entry.place(relx=0.05, rely=0.2, relwidth=0.8)
        
        self.quantity_label = ctk.CTkLabel(self.ui.content_frame, text="Quantity:", font=self.font14, text_color="white")
        self.quantity_label.place(relx=0.05, rely=0.3)
        
        self.quantity_entry = ctk.CTkEntry(self.ui.content_frame, placeholder_text="Enter quantity", font=self.font14)
        self.quantity_entry.place(relx=0.05, rely=0.35, relwidth=0.8)
        
        self.choose_graph_label = ctk.CTkLabel(self.ui.content_frame, text="Choose Graph ID:", font=self.font14, text_color="white")
        self.choose_graph_label.place(relx=0.05, rely=0.45)

        self.graph_optionmenu = ctk.CTkOptionMenu(self.ui.content_frame, values=self.graphs, font=self.font14,  fg_color="#343638", button_color="#565B5E", button_hover_color="#393A3B", dropdown_fg_color="#393939", dropdown_hover_color="#787878", text_color="white")
        self.graph_optionmenu.place(relx=0.05, rely=0.5, relwidth=0.8)

        self.submit_button = ctk.CTkButton(self.ui.content_frame, text="Add Pixel", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=lambda: self.add_pixel(self.hasGraphs))
        self.submit_button.place(relx=0.5, rely=0.65, anchor=CENTER, relwidth=0.3)

    def add_pixel(self, trySend=True):
        if not trySend:
            messagebox.showinfo("Info", "You have no graphs to add pixels. Please create a graph")
            return

        date = self.date_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        if not date or not quantity:
            messagebox.showerror("Error", "Please fill all fields")
            return

        # Validate date format YYYYMMDD and existence
        if not (len(date) == 8 and date.isdigit()):
            messagebox.showerror("Error", "Date must be in YYYYMMDD format")
            return
        try:
            datetime.strptime(date, "%Y%m%d")
        except Exception:
            messagebox.showerror("Error", "Invalid date")
            return

        # Get selected graph from option menu
        graph_id = None
        try:
            graph_id = self.graph_optionmenu.get()
        except Exception:
            graph_id = None

        if not graph_id or graph_id == "No Graphs Found":
            messagebox.showinfo("Info", "You have no graphs to add pixels. Please create a graph")
            return

        try:
            creds = get_creds()
            if not creds or "error" in creds:
                messagebox.showerror("Error", "Credentials not found. Please sign up or login first.")
                return
            headers = {"X-USER-TOKEN": creds["tokenID"]}
            response = core.add_pixel(graph_id, headers, quantity, date, creds.get("username"))
            if response.get("isSuccess"):
                messagebox.showinfo("Success", "Pixel added successfully")
                self.ui.show_screen("home")
            else:
                messagebox.showerror("Error", response.get("message", "Failed to add pixel"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

# ================== SettingsScreen ================= #
class CTkColorPicker(ctk.CTkFrame):
    """UI-only color picker that uses helper converters from Functions/colorPicker."""
    def __init__(self, master, initial_color="#8B5CF6", hover_factor=0.8, **kwargs):
        super().__init__(master, **kwargs)
        self.hover_factor = hover_factor
        self.font = ctk.CTkFont(size=12, family="Cascadia Code")

        self.preview = ctk.CTkFrame(self, width=120, height=80, corner_radius=12, fg_color=initial_color)
        self.preview.pack(padx=10, pady=(6, 10))

        ctk.CTkLabel(self, text="Hue", font=self.font).pack(anchor="w", padx=8)
        self.hue = ctk.CTkSlider(self, from_=0, to=360, command=lambda _=None: self._update_color())
        self.hue.pack(fill="x", padx=8, pady=(0, 6))

        ctk.CTkLabel(self, text="Saturation", font=self.font).pack(anchor="w", padx=8)
        self.sat = ctk.CTkSlider(self, from_=0, to=100, command=lambda _=None: self._update_color())
        self.sat.pack(fill="x", padx=8, pady=(0, 6))

        ctk.CTkLabel(self, text="Value", font=self.font).pack(anchor="w", padx=8)
        self.val = ctk.CTkSlider(self, from_=0, to=100, command=lambda _=None: self._update_color())
        self.val.pack(fill="x", padx=8, pady=(0, 6))

        self._set_from_hex(initial_color)
        self._update_color()

    def _set_from_hex(self, hex_color):
        if hex_to_hsv:
            h, s, v = hex_to_hsv(hex_color)
            self.hue.set(h)
            self.sat.set(s)
            self.val.set(v)

    def _update_color(self):
        if hsv_to_hex:
            h = self.hue.get()
            s = self.sat.get()
            v = self.val.get()
            self.fg_color = hsv_to_hex(h, s, v)
            if darker:
                self.hover_color = darker(self.fg_color, self.hover_factor)
            else:
                self.hover_color = self.fg_color
            self.preview.configure(fg_color=self.fg_color)

    def get_colors(self):
        return getattr(self, 'fg_color', '#8B5CF6'), getattr(self, 'hover_color', '#6946BD')

class SettingsScreen:
    def __init__(self, ui):
        self.ui = ui
        self.font14 = ctk.CTkFont(size=14, family="Cascadia Code")
        self.fg, self.hover, self.text = get_theme()
        self.home_img = ctk.CTkImage(dark_image=Image.open("assets/homebutton.png"))
        self.creds = get_creds()
        self.graphs = self.creds.get('graphID', [])        
        self.add_widgets()
   
    def add_widgets(self):
        self.title = ctk.CTkLabel(self.ui.content_frame, text="Settings", font=ctk.CTkFont(size=20, family="Cascadia Code"), text_color="white")
        self.title.place(relx=0.5, rely=0.05, anchor=CENTER)

        divider = ctk.CTkFrame(self.ui.content_frame, height=2, fg_color="gray30")
        divider.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.home_button = ctk.CTkButton(self.ui.content_frame, image=self.home_img, text="", font=ctk.CTkFont(size=12, family="Cascadia Code"), fg_color=self.fg, hover_color=self.hover, corner_radius=20, cursor="hand2", command=lambda: self.ui.show_screen("home"))
        self.home_button.place(relx=0.05, rely=0.05, anchor="w", relwidth=0.1)

        self.displayGraphLabel = ctk.CTkLabel(self.ui.content_frame, text="Display Graph:", font=self.font14, text_color="white")
        self.displayGraphLabel.place(relx=0.05, rely=0.15, anchor="w")

        self.displayGraphChooser = ctk.CTkOptionMenu(self.ui.content_frame, values=self.graphs, font=self.font14, fg_color="#343638", button_color="#565B5E", button_hover_color="#393A3B", dropdown_fg_color="#393939", dropdown_hover_color="#787878", text_color="white")
        self.displayGraphChooser.place(relx=0.05, rely=0.2, anchor="w", relwidth=0.8)
        # Button to save chosen graph as the current display graph
        self.save_graph_button = ctk.CTkButton(self.ui.content_frame, text="Set Display Graph", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.set_display_graph)
        self.save_graph_button.place(relx=0.5, rely=0.28, anchor=CENTER, relwidth=0.4)

        # Accent color picker
        try:
            initial_accent = self.creds.get("accent_color", "#8B5CF6")
        except Exception:
            initial_accent = "#8B5CF6"

        self.accent_label = ctk.CTkLabel(self.ui.content_frame, text="Accent Color:", font=self.font14, text_color="white")
        self.accent_label.place(relx=0.05, rely=0.36, anchor="w")

        self.color_picker = CTkColorPicker(self.ui.content_frame, initial_color=initial_accent, height=210)
        self.color_picker.place(relx=0.05, rely=0.39, relwidth=0.9)

        self.save_accent_button = ctk.CTkButton(self.ui.content_frame, text="Set Accent Color", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.set_accent_color)
        self.save_accent_button.place(relx=0.05, rely=0.90, anchor="w", relwidth=0.4)

        self.default_accent_button = ctk.CTkButton(self.ui.content_frame, text="Reset to Default", font=self.font14, fg_color=self.fg, hover_color=self.hover, text_color=self.text, corner_radius=20, cursor="hand2", command=self.default_accent_color)
        self.default_accent_button.place(relx=0.55, rely=0.90, anchor="w", relwidth=0.4)
    def set_display_graph(self):
        selected_graph = self.displayGraphChooser.get()
        update_creds(lastGraphID=selected_graph)
        
    def set_accent_color(self):
        try:
            fg, hover = self.color_picker.get_colors()
            update_creds(accent_color=fg)
            messagebox.showinfo("Success", "Accent color saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def default_accent_color(self):
        try:
            default = "#8B5CF6"
            # reset UI picker sliders and preview if present
            if hasattr(self, 'color_picker') and self.color_picker is not None:
                try:
                    self.color_picker._set_from_hex(default)
                    self.color_picker._update_color()
                except Exception:
                    pass
            update_creds(accent_color=default)
            messagebox.showinfo("Success", "Accent color reset to default")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
# ==================== Run ==================== #
if __name__ == "__main__":  
    # Launch UI immediately
    UI()