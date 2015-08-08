#!/usr/bin/env python
from flask import Flask, redirect, url_for
import random
app = Flask(__name__)

tops = []
bots = []

with open("top.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            tops.append(line.strip())

with open("bottom.txt") as f:
    for line in f:
        if len(line.strip()) > 0:
            bots.append(line.strip())

@app.route("/<int:t>/<int:b>")
@app.route("/r/<int:b>")
@app.route("/<int:t>/r")
@app.route("/r/r")
def smash(t=-1, b=-1):
    if t not in range(len(tops)):
        t = random.randrange(len(tops))
        return redirect(url_for(smash, t=t, b=b))
    if b not in range(len(bots)):
        b = random.randrange(len(bots))
        return redirect(url_for(smash, t=t, b=b))
    return "%s %s" % (tops[t], bots[b])

if __name__ == "__main__":
    app.run(debug=True)
