from flask import Flask, render_template, redirect, url_for, request
import random

app = Flask(__name__)

# Template for empty frames
EMPTY_FRAMES = {
    str(i): {"points": 0, "state": "o"} for i in range(1, 11)
}

players = {}
next_player_id = 1


def reset_frames():
    return {str(i): {"points": 0, "state": "o"} for i in range(1, 10 + 1)}


@app.route("/game")
def show_game():
    return render_template("game.html", players=players)


@app.route("/add_player")
def add_player():
    global next_player_id

    name = request.args.get("name", f"Player{next_player_id}")

    players[next_player_id] = {
        "name": name,
        "frames": reset_frames(),
        "current_frame": 1
    }

    next_player_id += 1
    return redirect(url_for("show_game"))


@app.route("/remove_player")
def remove_player():
    player_id = int(request.args.get("id"))
    if player_id in players:
        del players[player_id]
    return redirect(url_for("show_game"))


@app.route("/bowl")
def bowl():
    player_id = int(request.args.get("id"))

    if player_id not in players:
        return "Player not found"

    player = players[player_id]
    frames = player["frames"]
    current_frame = player["current_frame"]

    # Restart their game if done
    if current_frame > 10:
        player["frames"] = reset_frames()
        player["current_frame"] = 1
        return redirect(url_for("show_game"))

    dab = frames[str(current_frame)]

    throw1 = random.randint(1, 10)
    throw2 = 0
    throw3 = 0
    throw4 = 0

    # Throw 2 if not strike
    if throw1 != 10:
        throw2 = random.randint(1, 10 - throw1)

    # Mark strike/spare/open
    if throw1 == 10:
        dab["state"] = "x"
    elif throw2 == 10 - throw1:
        dab["state"] = "/"
    else:
        dab["state"] = "o"

    dab["points"] = throw1 + throw2

    # Frame 10 handling
    if current_frame == 10:
        if dab["state"] == "x":
            throw3 = random.randint(1, 10)
            throw4 = random.randint(1, 10)
            dab["points"] = throw1 + throw2 + throw3 + throw4
        elif dab["state"] == "/":
            throw3 = random.randint(1, 10)
            dab["points"] += throw3

    # Previous frame bonuses
    if current_frame != 1:
        prev = frames[str(current_frame - 1)]
        if prev["state"] in ["/", "x"]:
            prev["points"] += throw1 + throw2

    if current_frame >= 3:
        prev2 = frames[str(current_frame - 2)]
        if prev2["state"] == "x":
            prev2["points"] += throw1 + throw2

    player["current_frame"] += 1

    return redirect(url_for("show_game"))


if __name__ == '__main__':
    app.run(debug=True)
