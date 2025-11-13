from flask import Flask
import math

app = Flask(__name__)

frames = ({
          "1": {"points": 0, "state": "o"},
          "2": {"points": 0, "state": "o"},
          "3": {"points": 0, "state": "o"},
          "4": {"points": 0, "state": "o"},
          "5": {"points": 0, "state": "o"},
          "6": {"points": 0, "state": "o"},
          "7": {"points": 0, "state": "o"},
          "8": {"points": 0, "state": "o"},
          "9": {"points": 0, "state": "o"},
          "10": {"points": 0, "state": "o"} 
        })

current_frame = 1
#for value in frames.values():

@app.route("/game")
def show_game():
    return f"<p>{frames}</p>" 
    
@app.route("/bowl")
def bowl():
    this = frames[str(current_frame)]
    this["points"] = math.random(0, 10)
    this["state"] = "o"
    return f"<p>{this}</p>"
    