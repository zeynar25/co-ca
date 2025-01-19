# To do (For Nate)
# - Don't hardcode customize
# - Implement highscore 
#     - connect highscore to database
#     - create table for highscore = id username mode category difficulty datetime points
#     - add filter for difficulty and datetime (this week, this month, this year ganon)

# To do (For team Frontend)
# - Mananakal ako pag hindi pa sinimulan HTML+CSS

from flask import Flask, redirect, render_template, request, session

import random
import sqlite3

from classes.country import Country
from classes.question import Question
from classes.multiple_choice import MultipleChoice
from classes.true_false import TrueFalse


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

# Generate the quiz based on mode and category
@app.route("/quiz", methods=["GET"])
def quiz():
    # Retrieve values from session.
    mode = session.get('mode')  
    category = session.get('category') 
    difficulty = session.get('difficulty') 

    questions = []
    countries = get_countries_by_category(category)
    
    random.shuffle(countries)

    # First ten countries in the list will serve as the questions.
    for i in range(10): 
        if difficulty == "true-false":
            choices = ["True", "False"]
            answer = random.choice(choices)

            if mode == "name":
                country_used = countries[i].name

                if answer == "False":
                    while (country_used == countries[i].name):
                        country_used = random.choice(countries).name

                description = f"{countries[i].capital} is the capital city of {country_used}."
            else:
                capital_used = countries[i].capital

                if answer == "False":
                    while (capital_used == countries[i].capital):
                        capital_used = random.choice(countries).capital

                description = f"{capital_used} is the capital city of {countries[i].name}."
            
            question = TrueFalse(
                countries[i].id, 
                countries[i].name, 
                countries[i].capital, 
                countries[i].continent, 
                description, 
                answer
            )

        elif difficulty == "multiple-choice":
            answer_key = None

            if mode == "name":
                description = f"{countries[i].capital} is the capital of which city?"
                answer_key = countries[i].name
            else:
                description = f"What is the capital of {countries[i].name}?"
                answer_key = countries[i].capital
            
            question = MultipleChoice(
                countries[i].id, 
                countries[i].name, 
                countries[i].capital, 
                countries[i].continent, 
                description, 
                answer_key
            )
        
            question.add_options(countries, mode)

        else:
            answer_key = None

            if mode == "name":
                description = f"{countries[i].capital} is the capital of which city?"
                answer_key = countries[i].name
            else:
                description = f"What is the capital of {countries[i].name}?"
                answer_key = countries[i].capital
            
            question = Question(
                countries[i].id, 
                countries[i].name, 
                countries[i].capital, 
                countries[i].continent, 
                description, 
                answer_key
            )

        questions.append(question)

    # Convert questions to a list of dictionaries
    session['questions'] = [q.to_dict() for q in questions]

    return render_template('quiz.html', mode=mode, category=category, difficulty=difficulty, questions=questions)


# Check the quiz, and upload the score to highscore db.
# ask for a username
@app.route("/submit", methods=["POST"])
def check():
    mode = session.get('mode')  
    category = session.get('category') 
    difficulty = session.get('difficulty') 
    questions_data = session.get('questions')

    score = 0
    if difficulty == "true-false":
        questions = [TrueFalse(
            id=q['id'], 
            name=q['name'], 
            capital=q['capital'], 
            continent=q['continent'], 
            question=q['question'], 
            answer_key=q['answer_key']
        ) for q in questions_data]

    elif difficulty == "multiple-choice":
        questions = [MultipleChoice(
            id=q['id'], 
            name=q['name'], 
            capital=q['capital'], 
            continent=q['continent'], 
            question=q['question'], 
            answer_key=q['answer_key'], 
            options=q['options']
        ) for q in questions_data]

    else:
        questions = [Question(
            id=q['id'], 
            name=q['name'], 
            capital=q['capital'], 
            continent=q['continent'], 
            question=q['question'], 
            answer_key=q['answer_key']
        ) for q in questions_data]

    for i in range(10):
        answer = request.form.get(str(questions[i].id)) or "None"
        questions[i].answer = answer

        if (questions[i].answer == questions[i].answer_key):
            score += 1

    return render_template("score.html", mode=mode, category=category, difficulty=difficulty, score=score, questions=questions)


@app.route("/upload", methods=["POST"])
def upload():
    mode = session.get('mode')  
    category = session.get('category') 
    difficulty = session.get('difficulty') 

    username = request.form.get("username")
    score = int(request.form.get("score"))

    if difficulty == "true-false":
        score *= 2
    elif difficulty == "multiple-choice":
        score *= 5
    else:
        score *= 10

    # get current datetime and assign on a variable

    # Create player object based on credentials
    #   id username mode category difficulty datetime
    # Upload to highscore table

    return redirect("/quiz")

@app.route("/highscore", methods=["POST", "GET"])
def highscore():
    if request.method == "POST":
        players = []

        # get filters applied
        # create a query out of it, top 10 nalang

    # query for top 100 players of all mode, category, and difficulty and history

    return render_template("highscore.html", players=players)

if __name__ == "__main__":
    app.run(debug=True)