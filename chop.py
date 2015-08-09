#!/usr/bin/env python
from flask import Flask, redirect, url_for, render_template
import random
app = Flask(__name__)

tops = [""]
bots = [""]

with open("top.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            tops.append(line.strip())
print("%i tops loaded" % (len(tops)-1))

with open("bottom.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            if not line.strip().endswith("."):
                line = line.strip() + "."
            bots.append(line)
print("%i bottoms loaded" % (len(bots)-1))

@app.route("/api/<int:t>/<int:b>")
@app.route("/api/r/<int:b>")
@app.route("/api/<int:t>/r")
@app.route("/api/r/r")
def api_smash(t=0, b=0):
    if t not in range(1, len(tops)):
        t = random.randrange(1, len(tops))
        return redirect(url_for("api_smash", t=t, b=b))
    if b not in range(1, len(bots)):
        b = random.randrange(1, len(bots))
        return redirect(url_for("api_smash", t=t, b=b))
    if t == b:
        return random.choice([redirect(url_for("api_smash", t=random.randrange(1, len(tops)), b=b)), redirect(url_for("api_smash", t=t, b=random.randrange(1, len(bots))))])
    boom = "%s %s" % (tops[t], bots[b])
    print(boom)
    return boom

@app.route("/<int:t>/<int:b>")
@app.route("/r/<int:b>")
@app.route("/<int:t>/r")
@app.route("/r/r")
@app.route("/")
def smash(t=0, b=0):
    if t not in range(1, len(tops)):
        return redirect(url_for("smash", t=random.choice([x for x in range(1, len(tops)) if x != b]), b=b))
    if b not in range(1, len(bots)):
        return redirect(url_for("smash", t=t, b=random.choice([x for x in range(1, len(bots)) if x != t])))
    if t == b:
        return random.choice([redirect(url_for("smash", t=random.choice([x for x in range(1, len(tops)) if x != b]), b=b)), redirect(url_for("smash", t=t, b=random.choice([x for x in range(1, len(bots)) if x != t])))])
    boom = "%s %s" % (tops[t], bots[b])
    print(boom)
    return render_template("home.html", ka=tops[t], boom=bots[b], t=t, b=b)

if __name__ == "__main__":
    app.run(debug=True)
