from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return "This is the homepage: %s" % request.method

@app.route("/tuna")
def tuna():
	return "<h2>Tuna is good</h2>"

@app.route("/profile/<username>")
def profile(username):
	return "<h1>Hey there %s</h1>" % username

@app.route("/post/<int:post_id>")
def post(post_id):
	return "<h2>Post ID is %s</h2>" % post_id

@app.route("/bacon", methods=["GET", "POST"])
def bacon():
	if request.method == "POST":
		return "You are using POST"
	else:
		return "You are using GET"

@app.route("/shop")
@app.route("/shop/<name>")
def shop(name=None):
	return render_template("shop.html", name=name)

@app.route("/shopping")
def shopping():
	food = ["cheese", "tuna", "bacon", "popcorn"]
	return render_template("shopping.html", food=food)

if __name__ == "__main__":
	app.run(debug=True)



