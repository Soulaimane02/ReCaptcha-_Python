from tkinter import *
import random
from flask import Flask, request, abort

app = Flask(__name__)

@app.before_request
def block_scrapers():
    user_agent = request.headers.get('User-Agent')
    banned_agents = ['Scrapy', 'PostmanRuntime', 'python-requests', 'Selenium']
    if any(bot in user_agent for bot in banned_agents):
        abort(403)

@app.route("/")
def home():
    # Fenêtre principale
    fenetre = Tk()
    fenetre.geometry('600x600')
    fenetre.title('Draw the Path - Real Challenge')
    fenetre['bg'] = '#f0f0f0'
    fenetre.resizable(height=False, width=False)

    # Canvas pour dessiner
    canvas = Canvas(fenetre, bg="white", width=500, height=500, highlightthickness=2, highlightbackground="black")
    canvas.pack(pady=20)

    # Variables globales
    game_state = {
        "path_limits": [],
        "end_zone": None,
        "prev_x": None,
        "prev_y": None,
        "game_won": False,
        "successes": 0,
        "attempts": 0,
        "lives": 3
    }

    # Création du parcours
    def create_path():
        canvas.delete("all")
        game_state["path_limits"] = []

        path_coords = [
            (50, 50, 150, 50, 150, 100, 50, 100),
            (150, 50, 250, 50, 250, 100, 150, 100),
            (250, 50, 350, 150, 300, 200, 250, 100),
            (350, 150, 400, 300, 350, 350, 300, 200),
            (400, 300, 350, 400, 250, 450, 200, 400),
        ]

        for coords in path_coords:
            path_part = canvas.create_polygon(coords, fill="blue", outline="black", width=2)
            game_state["path_limits"].append(coords)

        # Zone de fin
        game_state["end_zone"] = canvas.create_oval(190, 390, 210, 410, fill="red", outline="black")

    # Détection de sortie de parcours
    def is_out_of_path(x, y):
        # Vérifie si le point (x, y) est dans un des polygones du parcours
        for coords in game_state["path_limits"]:
            if point_in_polygon(x, y, coords):
                return False
        return True
    def point_in_polygon(x, y, polygon):
        n = len(polygon) // 2
        inside = False
        p1x, p1y = polygon[0], polygon[1]
        for i in range(n + 1):
            p2x, p2y = polygon[(i % n) * 2], polygon[(i % n) * 2 + 1]
            if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def display_message(message, color):
        canvas.create_text(250, 250, text=message, font=("Arial", 18, "bold"), fill=color)

    # Détection de victoire
    def check_win(event):
        if not game_state["game_won"] and canvas.coords(game_state["end_zone"])[0] <= event.x <= \
                canvas.coords(game_state["end_zone"])[2] \
                and canvas.coords(game_state["end_zone"])[1] <= event.y <= canvas.coords(game_state["end_zone"][3]):
            game_state["game_won"] = True
            game_state["successes"] += 1
            display_message("Bravo ! Vous avez réussi cette manche.", "blue")
            fenetre.after(2000, next_round)

    def start_draw(event):
        game_state["prev_x"], game_state["prev_y"] = event.x, event.y

    def draw_line(event):
        if game_state["prev_x"] is not None and game_state["prev_y"] is not None:
            canvas.create_line(game_state["prev_x"], game_state["prev_y"], event.x, event.y, fill="black", width=3)

        if is_out_of_path(event.x, event.y):
            game_state["lives"] -= 1
            if game_state["lives"] > 0:
                display_message(f"Vous avez quitté le parcours ! Vies restantes : {game_state['lives']}", "red")
                fenetre.after(2000, next_round)
            else:
                display_message("Vous avez échoué au CAPTCHA.", "red")
                fenetre.after(2000, fenetre.destroy)
            return

        game_state["prev_x"], game_state["prev_y"] = event.x, event.y
        check_win(event)

    # Arrêt du dessin
    def stop_draw(event):
        game_state["prev_x"], game_state["prev_y"] = None, None

    # Prochaine manche ou fin de jeu
    def next_round():
        if game_state["successes"] >= 3:
            display_message("CAPTCHA validé avec succès !", "green")
            fenetre.after(2000, fenetre.destroy)
            return  # Fin du jeu (CAPTCHA validé)

        game_state["attempts"] += 1
        game_state["game_won"] = False
        create_path()

    create_path()

    canvas.bind("<Button-1>", start_draw)
    canvas.bind("<B1-Motion>", draw_line)
    canvas.bind("<ButtonRelease-1>", stop_draw)

    fenetre.mainloop()



if __name__ == "__main__":
    home()
