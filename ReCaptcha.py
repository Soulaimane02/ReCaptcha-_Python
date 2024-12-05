from tkinter import *
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
    fenetre = Tk()
    fenetre.geometry('400x400')
    fenetre.title('Captcha-python')
    fenetre['bg'] = 'grey'
    fenetre.resizable(height=False, width=False)

    fenetre.mainloop()


if __name__ == "__main__":
    home()