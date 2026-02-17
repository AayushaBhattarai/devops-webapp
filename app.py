from flask import Flask, render_template, request, redirect
from datetime import date
import csv

app = Flask(__name__)

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ADD EXPENSE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        today = date.today()

        with open("expenses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([today, amount, category])

        return redirect("/")

    return render_template("add.html")


# VIEW EXPENSES
@app.route("/view")
def view():
    expenses = []
    total = 0

    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 3:
                    continue

                date_val, amount, category = row
                amount = int(amount)

                expenses.append({
                    "date": date_val,
                    "amount": amount,
                    "category": category
                })

                total += amount

    except FileNotFoundError:
        pass

    return render_template("view.html", expenses=expenses, total=total)


if __name__ == "__main__":
    app.run(debug=True)
