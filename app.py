# To do
# 1. Implement filter in highscore (for Nate)
# 2. Implement queries (for Team SQL)
# 3. Design with CSS (for Team Frontend)

from flask import Flask, redirect, render_template, request, session
import random

from classes.country import Country
from classes.question import Question


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'uno-sa-oop'


# Displays Play and highscore button.
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html') 


# Render guess the capital or country questions.
@app.route("/mode", methods=["GET", "POST"])
def mode():
    if request.method == "POST":
        selected_mode = request.form.get("mode")
        session['mode'] = selected_mode
        return redirect("/category")
    
    return render_template("mode.html")


# Render all and continents buttons.
@app.route("/category", methods=["GET", "POST"])
def category():
    if request.method == "POST":
        selected_categ = request.form.get("category")
        session['category'] = selected_categ
        return redirect("/quiz")
    
    return render_template("category.html")


# Generate the quiz based on mode and category
@app.route("/quiz", methods=["GET"])
def quiz():
    # Retrieve values from session.
    mode = session.get('mode')  
    category = session.get('category') 

    questions = []

    # Change this part SQL team, retrive niyo entries where continent = category;
    # Lagyan niyo ng condition na if category == "all", wala ng where clause.
    # tas convert niyo to a list of Country objects.
    ph = Country(1,"Philippines", "Manila", "Asia")
    jp = Country(2, "Japan", "Tokyo", "Asia")
    sk = Country(3, "South Korea", "Seoul", "Asia")
    nk = Country(4, "North Korea", "Pyeongyang", "Asia")
    ch = Country(5, "China", "Beijing", "Asia")
    rs = Country(6, "Russia", "Moscow", "Asia")
    nd = Country(7, "India", "Delhi", "Asia")
    ml = Country(8, "Malaysia", "Kuala Lumpur", "Asia")
    countries = [ph, jp, sk, nk, ch, rs, nd, ml]

    # Generate 8 questions.
    # Replace with 10 once program is connected to database.
    while len(questions) < 8:
        curr = random.choice(countries)

        # Check if curr already exist as a question
        skip = False
        for q in questions :
            if q.name == curr.name:
                skip = True
                break

        if skip:
            continue

        question = Question(curr.id, curr.name, curr.capital, curr.continent)

        if mode == "capitals":
            question.add_option(curr.capital)
            while len(question.options) < 4:
                curr2 = random.choice(countries)

                # Skip when curr2.capital already exist in option.
                skip2 = False
                for option in question.options :
                    if option == curr2.capital:
                        skip2 = True
                        break

                if skip2:
                    continue
                else:
                    question.add_option(curr2.capital)

        else:
            question.add_option(curr.name)
            while len(question.options) < 4:
                curr2 = random.choice(countries)

                # Skip when curr2.capital already exist in option.
                skip2 = False
                for option in question.options :
                    if option == curr2.name:
                        skip2 = True
                        break

                if skip2:
                    continue
                else:
                    question.add_option(curr2.name)

        random.shuffle(question.options)
        questions.append(question)

    # Convert questions to a list of dictionaries
    session['questions'] = [q.to_dict() for q in questions]

    return render_template('quiz.html', mode=mode, category=category, questions=questions)


# Check the quiz, and upload the score to highscore db.
# ask for a username
# try adding a datetime for highscore
@app.route("/submit", methods=["POST"])
def check():
    mode = session.get('mode')  
    questions_data = session.get('questions')

    score = 0

    # Convert session questions back to a list of Question object.
    questions = [Question(**q) for q in questions_data]

    # replace 8 with 10 later on
    for i in range(8):
        answer = request.form.get(str(questions[i].id)) or "None"
        questions[i].user_answer = answer

        if mode == "capitals":
            questions[i].correct_answer = questions[i].capital
        else:
            questions[i].correct_answer = questions[i].name

        if (answer == questions[i].correct_answer):
            score += 1

    return render_template("score.html", score=score, questions=questions)


@app.route("/highscore", methods=["POST", "GET"])
def highscore():
    filter = "all"

    # Team SQL gawa kayo query dito top 10 score based sa filter
    players = [{"username" : "Nate", "score" : 10}, {"username" : "Samuel", "score" : 0}]
    if request.method == "POST":
        username = request.form.get("username")
        score = request.form.get("score")

        if username is not None:
            player = {"username": username, "score": int(score)}
            players.append(player)
            # up niyo to sa database

        else:
            filter = request.form.get("filter") or "all"

            # update niyo yung query based sa laman nung filter variable.

    return render_template("highscore.html", players=players, filter=filter)

if __name__ == "__main__":
    app.run(debug=True)