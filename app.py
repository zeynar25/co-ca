# To do (For Nate)
# - modify classes
#   - add subclasses to question.py (trueorfalse, identification?)

# - Implement trueorfalse and identification difficulty in quiz 
# - Implement highscore 
#     - connect highscore to database
#     - create table for highscore = id username difficulty datetime points
#     - add filter for difficulty and datetime (this week, this month, this year ganon)

# To do (For team Frontend)
# - Mananakal ako pag hindi pa sinimulan HTML+CSS

# To do (For team database)
# - Palagyan na laman countries sa Africa

from flask import Flask, redirect, render_template, request, session

import random
import sqlite3

from classes.country import Country
from classes.question import Question
from classes.multiple_choice import MultipleChoice


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'uno-sa-oop'


# Displays Play and highscore button.
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html') 


# Render guess the capital or country questions.
@app.route("/customize", methods=["GET", "POST"])
def customize():
    if request.method == "POST":
        selected_mode = request.form.get("mode")
        selected_categ = request.form.get("category")
        selected_difficulty = request.form.get("difficulty")

        session['mode'] = selected_mode
        session['category'] = selected_categ
        session['difficulty'] = selected_difficulty

        return redirect("/quiz")
    
    return render_template("customize.html")

def get_countries_by_category(category):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if category == "Earth":
        query = cursor.execute('select id, country, capital, continent from countries')
    else:
        query = cursor.execute('select id, country, capital, continent from countries where continent = ?', (category,))

    result = query.fetchall()

    connection.commit()
    connection.close()

    return [Country(*row) for row in result]

def add_options(question, countries, attribute):
    options = set()
    options.add(getattr(question, attribute))

    while len(options) < 4:
        random_country = random.choice(countries)
        options.add(getattr(random_country, attribute))
    
    question.options = list(options)
    random.shuffle(question.options)

# Generate the quiz based on mode and category
@app.route("/quiz", methods=["GET"])
def quiz():
    # Retrieve values from session.
    mode = session.get('mode')  
    category = session.get('category') 
    difficulty = session.get('difficulty') 

    questions = []
    countries = get_countries_by_category(category)
    
    # Generate 10 questions
    random.shuffle(countries)
    for i in range(10): 
        if difficulty == "multiple-choice":
            if mode == "name":
                desc = f"{countries[i].capital} is the capital of which city?"
                question = MultipleChoice(
                    countries[i].id, 
                    countries[i].name, 
                    countries[i].capital, 
                    countries[i].continent, 
                    desc, 
                    countries[i].name
                )
            else:
                desc = f"What is the capital of {countries[i].name}?"
                question = MultipleChoice(
                    countries[i].id, 
                    countries[i].name, 
                    countries[i].capital, 
                    countries[i].continent, 
                    desc, 
                    countries[i].capital)
        
            add_options(question, countries, mode)

        questions.append(question)

    # Convert questions to a list of dictionaries
    session['questions'] = [q.to_dict() for q in questions]
    print(session['questions'])

    return render_template('quiz.html', mode=mode, category=category, difficulty=difficulty, questions=questions)


# Check the quiz, and upload the score to highscore db.
# ask for a username
# try adding a datetime for highscore
@app.route("/submit", methods=["POST"])
def check():
    mode = session.get('mode')  
    difficulty = session.get('difficulty') 
    questions_data = session.get('questions')

    score = 0

    if difficulty == "multiple-choice":
        # Convert session questions back to a list of Question object.
        questions = [MultipleChoice(
            id=q['id'], 
            name=q['name'], 
            capital=q['capital'], 
            continent=q['continent'], 
            desc=q['desc'], 
            answer_key=q['answer_key'], 
            options=q['options']
        ) for q in questions_data]

        for i in range(10):
            answer = request.form.get(str(questions[i].id)) or "None"
            questions[i].answer = answer

            if (answer == questions[i].answer_key):
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