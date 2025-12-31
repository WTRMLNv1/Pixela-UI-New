# Pixela 🖌️

**Pixela** is a desktop application built with **Python** and **CustomTkinter** that allows users to **track habits, create graphs, and visualize their productivity** in a sleek, interactive interface. Perfect for anyone who loves data, visuals, or just wants to see their progress over time!  

---

## Features ✨

- **User Accounts:** Login/Sign up system with persistent credentials.  
- **Graph Creation:** Easily create custom graphs with units, types, and colors.  
- **Add Pixels:** Track daily activities or data points in your graphs.  
- **Dynamic Heatmap:** Visualize your data at a glance.  
- **Custom Accent Colors:** Personalize the app with your favorite colors using an interactive HSV color picker.  
- **Settings Screen:** Set your preferred graph for display and manage accent colors.  
- **Responsive UI:** Clean, modern, and consistent design.  

---

## Screenshots 📸

*Include some of your app screenshots here (Home, Add Pixel, Graph, Settings)*  

---

## Installation ⚡

1. Clone this repo:  
```bash
git clone https://github.com/yourusername/Pixela.git
cd Pixela
```
2. Install Dependancies
```bash
pip install -r requirements.txt
```
Or Download manually:
```bash
pip install customtkinter
pip install Pillow
pip install matplotlib
pip install numpy
pip install requests
```
3. Run the app
```bash
python UI.py
```

## Usage 🛠️
- Open the app, login or sign up 
- Create a graph with your preferred name, unit, and color.
- Add daily pixels to track your progress.
- Customize your accent color in Settings.
- View your heatmap on the Home screen.

## Project Structure 📂
```graphql
Pixela/
│
├─ assets/              # Icons and images used in the app
├─ Functions/           # Core logic and helper modules
├─ Save_chart.py        # Handles heatmap saving
├─ UI.py                # Main UI module
└─ README.md            # This file
```