from flask import Flask, render_template, redirect, url_for
import random

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
    return render_template("game.html", frames=frames, current_frame=current_frame)
    
@app.route("/bowl")
def bowl():
    global current_frame
    if current_frame > 10:
        current_frame = 1
        return redirect(url_for("show_game"))
    
    if current_frame == 1:
        for frame in frames:
            frames[f"{frame}"]["points"] = 0
            frames[f"{frame}"]["state"] = "o"

    dab = frames[str(current_frame)]
    throw1 = random.randint(1, 10)
    throw2 = 0
    throw3 = 0
    throw4 = 0
    if throw1 != 10:
        throw2 = random.randint(1, 10 - throw1)
    if throw1 == 10:
        dab["points"] = 10
        dab["state"] = "x"
    elif throw2 == 10-throw1:
        dab["state"] = "/"
    else:
        dab["state"] = "o"
    dab["points"] = throw1 + throw2
    if current_frame == 10:
        if dab["state"] == "x":
            throw3 = random.randint(1, 10)
            dab["points"] = throw1 + throw2 + throw3
            throw4 = random.randint(1, 10)
            dab["points"] = throw1 + throw2 + throw3 + throw4
        if dab["state"] == "/":
            throw3 = random.randint(1, 10)
            dab["points"] += throw3
    if current_frame != 1:
        if frames[str(current_frame - 1)]["state"] == "/" or frames[str(current_frame - 1)]["state"] == "x":
            temp = frames[str(current_frame-1)]["points"]
            frames[str(current_frame-1)]["points"] = temp + throw1 + throw2
    if current_frame != 2 and current_frame != 1:
        if frames[str(current_frame - 2)]["state"] == "x":
            temp = frames[str(current_frame-2)]["points"]
            if current_frame == 10:
                frames[str(current_frame-2)]["points"] = temp + throw1 + throw2 + throw3
            else:
                frames[str(current_frame-2)]["points"] = temp + throw1 + throw2
    current_frame += 1
    return redirect(url_for("show_game"))


if __name__ == '__main__':
    app.run()