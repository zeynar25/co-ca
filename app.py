# To do (For Nate)
# - Add features to highscore 
#     - add 4 more queries, annually, monthly, weekly, daily based on record_date
#     - add filter for mode, category, and option

from flask import Flask, redirect, render_template, request, session

import random
import sqlite3
from datetime import datetime

from classes.country import Country
from classes.question import Question
from classes.multiple_choice import MultipleChoice
from classes.true_false import TrueFalse
from classes.player import Player


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
        
        if selected_mode == "Capital city":
            selected_mode = "capital"
        elif selected_mode == "Country":
            selected_mode = "name"

        selected_categ = request.form.get("category")

        selected_option = request.form.get("option")

        session['mode'] = selected_mode
        session['category'] = selected_categ
        session['option'] = selected_option

        return redirect("/quiz")
    
    mode = ["Capital city", "Country"]
    category = ["Earth", "Asia", "Africa", "North America", "South America", "Europe", "Australia"]
    option = ["True or False", "Multiple Choice", "Identification"]

    return render_template("customize.html", modes=mode, categories=category, options=option)

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
    option = session.get('option') 

    questions = []
    countries = get_countries_by_category(category)
    
    random.shuffle(countries)

    # First ten countries in the list will serve as the questions.
    for i in range(10): 
        if option == "True or False":
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

        elif option == "Multiple Choice":
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
    session['datetime_start'] = datetime.now()

    return render_template('quiz.html', mode=mode, category=category, option=option, questions=questions)


# Check the quiz, and upload the score to highscore db.
# ask for a username
@app.route("/submit", methods=["POST"])
def check():
    mode = session.get('mode')  
    category = session.get('category') 
    option = session.get('option') 
    questions_data = session.get('questions')

    score = 0
    if option == "True or False":
        questions = [TrueFalse(
            id=q['id'], 
            name=q['name'], 
            capital=q['capital'], 
            continent=q['continent'], 
            question=q['question'], 
            answer_key=q['answer_key']
        ) for q in questions_data]

    elif option == "Multiple Choice":
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

    return render_template("score.html", mode=mode, category=category, option=option, score=score, questions=questions)


@app.route("/upload", methods=["POST"])
def upload():
    mode = session.get('mode')  
    category = session.get('category') 
    option = session.get('option') 
    datetime_start = session.get('datetime_start').replace(tzinfo=None)
    datetime_end = datetime.now().replace(tzinfo=None)

    user = request.form.get("username")
    score = int(request.form.get("score"))
    duration = datetime_end - datetime_start
    record_date = datetime_end.strftime("%Y-%m-%d")

    if option == "True or False":
        score *= 2
    elif option == "Multiple Choice":
        score *= 5
    else:
        score *= 10

    # upload results to database.
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f"insert into highscore(user, score, mode, category, option, duration, record_date) values('{user}', {score}, '{mode}', '{category}', '{option}', '{duration}', '{record_date}')")
    connection.commit()
    connection.close()

    return redirect("/highscore")

@app.route("/highscore", methods=["POST", "GET"])
def highscore():
    # When a filter is applied
    if request.method == "POST":
        ...
        # get filters applied
        # create a query out of it, top 10 nalang

    # query for top 100 players of all mode, category, and option and history

    # add 4 more queries, annually, monthly, weekly, daily based on record_date
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    query_all = '''SELECT id, user, score, mode, category, option, duration, record_date 
        FROM highscore 
        ORDER BY score desc, duration 
        LIMIT 100'''
    
    result_all = cursor.execute(query_all).fetchall()
    

    query_annually = '''SELECT id, user, score, mode, category, option, duration, record_date 
        FROM highscore 
        WHERE strftime('%Y', record_date) = strftime('%Y', 'now')
        ORDER BY score desc, duration 
        LIMIT 100'''
    
    result_annually = cursor.execute(query_annually).fetchall()

    query_monthly = '''SELECT id, user, score, mode, category, option, duration, record_date 
        FROM highscore 
        WHERE strftime('%Y', record_date) = strftime('%Y', 'now')
            AND strftime('%m', record_date) = strftime('%m', 'now')
        ORDER BY score desc, duration 
        LIMIT 50'''
    
    result_monthly = cursor.execute(query_monthly).fetchall()

    query_weekly = '''SELECT id, user, score, mode, category, option, duration, record_date 
        FROM highscore 
        WHERE julianday('now') - julianday(record_date) <= 7
        ORDER BY score desc, duration 
        LIMIT 10'''

    result_weekly = cursor.execute(query_weekly).fetchall()
    connection.commit()
    connection.close()


    ranker_all = [Player(*row) for row in result_all]
    ranker_annually = [Player(*row) for row in result_annually]
    ranker_monthly = [Player(*row) for row in result_monthly]
    ranker_weekly = [Player(*row) for row in result_weekly]

    data = {"mode": "All Mode", "category": "All Category", "option": "All Option"}

    return render_template("highscore.html", ranker_all=ranker_all, ranker_annually=ranker_annually, ranker_monthly=ranker_monthly, ranker_weekly=ranker_weekly, data=data)

if __name__ == "__main__":
    app.run(debug=True)