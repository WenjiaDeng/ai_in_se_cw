import os
from datetime import datetime

from flask import Flask, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Alice1234@127.0.0.1:3306/canteendb?charset=utf8"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)


class Dishes(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pic = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    type = db.Column(db.String(20))


class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100))
    Dishname = db.Column(db.String(100))
    Ordertime = db.Column(db.DateTime)
    status = db.Column(db.Boolean)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/dishes", methods=["GET"])
def dishes():
    foods = Dishes.query.all()
    return render_template("dishes.html", foods=foods)


@app.route("/submitfood", methods=["POST"])
def submitfood():
    dishname = request.form.get("food")
    now = datetime.now()

    od = Orders(
        Username="Alice",
        Dishname=dishname,
        Ordertime=now,
        status=False
    )
    db.session.add(od)
    db.session.commit()

    return f"Order received: {dishname} at {now}"


@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        orderid = request.form.get("orderid")
        od = Orders.query.get(orderid)
        if od:
            od.status = True
            db.session.commit()
            return f"Order completed: id={od.id}, dish={od.Dishname}"
        return "Order not found."

    ods = Orders.query.all()
    return render_template("orders.html", ods=ods)


@app.route("/adddata", methods=["GET"])
def adddata():
    db.create_all()

    created = False

    if Dishes.query.count() == 0:
        sample_dishes = [
            Dishes(name="Apple", pic="apple.jpg", description="Fresh red apple", price=10),
            Dishes(name="Banana", pic="banana.jpg", description="Sweet yellow banana", price=20),
            Dishes(name="Meatball", pic="meatball.jpg", description="Pork kneaded into balls", price=30),
            Dishes(name="Steamed Fish", pic="fish.jpg", description="Fresh steamed fish with light sauce", price=40),
            Dishes(name="Roast Duck", pic="duck.jpg", description="Crispy roast duck with rich flavour", price=50),
        ]
        db.session.add_all(sample_dishes)
        created = True

    if Users.query.count() == 0:
        sample_users = [
            Users(username="Alice", password_hash="abcd1234", description="Customer user", type="customer"),
            Users(username="Bob", password_hash="123456", description="Chef user", type="chef"),
        ]
        db.session.add_all(sample_users)
        created = True

    if created:
        db.session.commit()
        return "data added!"
    return "sample data already exists!"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)