#!/usr/bin/env python
from flask import Flask, redirect, url_for, render_template, jsonify
from porc import Client
from humanize import intword
from secrets import ORCHESTRATE_KEY
import random
app = Flask(__name__)
app.config["SERVER_NAME"] = "chopmotto.ml"
orche = Client(ORCHESTRATE_KEY, "https://api.aws-eu-west-1.orchestrate.io/")
orche.ping().raise_for_status()

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
        return redirect(url_for("api_smash", t=t, b=b, _external=True, _scheme="https"))
    if b not in range(1, len(bots)):
        b = random.randrange(1, len(bots))
        return redirect(url_for("api_smash", t=t, b=b, _external=True, _scheme="https"))
    if t == b:
        return random.choice([redirect(url_for("api_smash", t=random.randrange(1, len(tops)), b=b, _external=True, _scheme="https")), redirect(url_for("api_smash", t=t, b=random.randrange(1, len(bots)),_external=True, _scheme="https"))])
    boom = "%s %s" % (tops[t], bots[b])
    print(boom)
    return boom

@app.route("/api/slack", methods=["GET","POST"])
def api_slack():
    t = random.randrange(1, len(tops))
    b = random.randrange(1, len(bots))
    while t == b:
        if round(random.random(), 0) == 1.0:
            t = random.randrange(1, len(tops))
        else:
            b = random.randrange(1, len(bots))
    return jsonify(response_type="in_channel", text=("%s %s" % (tops[t], bots[b])).strip())

@app.route("/like/<int:t>/<int:b>")
def like(t, b):
    orche.post_event("quotes", "%i/%i"%(t,b), "liking", {})
    return redirect(url_for("smash", t=t, b=b, _external=True, _scheme="https"))

@app.route("/<int:t>/<int:b>")
@app.route("/r/<int:b>")
@app.route("/<int:t>/r")
@app.route("/r/r")
def smash(t=0, b=0):
    if t not in range(1, len(tops)):
        return redirect(url_for("smash", t=random.choice([x for x in range(1, len(tops)) if x != b]), b=b, _external=True, _scheme="https"))
    if b not in range(1, len(bots)):
        return redirect(url_for("smash", t=t, b=random.choice([x for x in range(1, len(bots)) if x != t]), _external=True, _scheme="https"))
    if t == b:
        return random.choice([redirect(url_for("smash", t=random.choice([x for x in range(1, len(tops)) if x != b]), b=b, _external=True, _scheme="https")), redirect(url_for("smash", t=t, b=random.choice([x for x in range(1, len(bots)) if x != t]),_external=True, _scheme="https"))])
    boom = "%s %s" % (tops[t], bots[b])
    print(boom)
    return render_template("home.html", ka=tops[t], boom=bots[b], t=t, b=b, l=len(orche.list_events("quotes", "%i/%i"%(t,b), "liking").all()), naturalsize=intword)

@app.route("/")
def cta():
    return render_template("cta.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
