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

def fetch_highscores(filters=None, limit=100, time_filter=None):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    base_query = "SELECT id, user, score, mode, category, option, duration, record_date FROM highscore"
    params = []

    if filters:
        conditions = []
        if filters.get("mode") and filters["mode"] != "All":
            conditions.append("mode = ?")
            params.append(filters["mode"])

        if filters.get("category") and filters["category"] != "All":
            conditions.append("category = ?")
            params.append(filters["category"])

        if filters.get("option") and filters["option"] != "All":
            conditions.append("option = ?")
            params.append(filters["option"])

        base_query += " WHERE " + " AND ".join(conditions)

    if time_filter:
        base_query += f" AND {time_filter}"

    base_query += f" ORDER BY score DESC, duration LIMIT {limit}"

    result = cursor.execute(base_query, params).fetchall()
    connection.close()

    return result


# Landing page: displays play and highscore button.
@app.route("/", methods=["GET", "POST"])
def index():
    # Filter choices.
    modes = ["All", "Capital city", "Country"]
    categories = ["All", "Earth", "Asia", "Africa", "North America", "South America", "Europe", "Australia"]
    options = ["All", "True or False", "Multiple Choice", "Identification"]

    # When a filter is applied.
    if request.method == "POST":
        mode = request.form.get("mode")
        category = request.form.get("category")
        option = request.form.get("option")

        # Place the filter applied at the top of each list
        modes.remove(mode)
        categories.remove(category)
        options.remove(option)

        modes.insert(0, mode)
        categories.insert(0, category)
        options.insert(0, option)

        if mode == "Capital city":
            mode = "capital"
        elif mode == "Country":
            mode = "country"

        # Get the list of highscores.
        result_all = fetch_highscores(filters={}, limit=100)
        result_annually = fetch_highscores(filters={}, limit=100, time_filter="strftime('%Y', record_date) = strftime('%Y', 'now')")
        result_monthly = fetch_highscores(filters={}, limit=50, time_filter="strftime('%Y-%m', record_date) = strftime('%Y-%m', 'now')")
        result_weekly = fetch_highscores(filters={}, limit=10, time_filter="julianday('now') - julianday(record_date) <= 7")

        # Map result to Player objects
        ranker_all = [Player(*row) for row in result_all]
        ranker_annually = [Player(*row) for row in result_annually]
        ranker_monthly = [Player(*row) for row in result_monthly]
        ranker_weekly = [Player(*row) for row in result_weekly]

        # Convert mode to its aesthetic version.
        if mode == "name":
            mode = "Country"
        elif mode == "capital":
            mode = "Capital"

        # Will be used as labels.
        data = {"mode": mode, "category": category, "option": option}
        data["mode"] += " Mode"
        data["category"] += " Category"
        data["option"] += " Option"

        return render_template(
            "index.html", 
            ranker_all=ranker_all, 
            ranker_annually=ranker_annually, 
            ranker_monthly=ranker_monthly, 
            ranker_weekly=ranker_weekly, 
            data=data, 
            modes=modes, 
            categories=categories, 
            options=options
        )

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    query = '''SELECT id, user, score, mode, category, option, duration, record_date 
        FROM highscore '''
    
    result_all = cursor.execute(query + "ORDER BY score desc, duration LIMIT 100").fetchall()

    result_annually = cursor.execute(query + "WHERE strftime('%Y', record_date) = strftime('%Y', 'now') ORDER BY score desc, duration LIMIT 100").fetchall()
    
    result_monthly = cursor.execute(query + "WHERE strftime('%Y', record_date) = strftime('%Y', 'now') AND strftime('%m', record_date) = strftime('%m', 'now') ORDER BY score desc, duration LIMIT 50").fetchall()

    result_weekly = cursor.execute(query + "WHERE julianday('now') - julianday(record_date) <= 7 ORDER BY score desc, duration LIMIT 10").fetchall()

    connection.commit()
    connection.close()

    ranker_all = [Player(*row) for row in result_all]
    ranker_annually = [Player(*row) for row in result_annually]
    ranker_monthly = [Player(*row) for row in result_monthly]
    ranker_weekly = [Player(*row) for row in result_weekly]

    data = {"mode": "All Mode", "category": "All Category", "option": "All Option"}

    return render_template(
        "index.html", 
        ranker_all=ranker_all, 
        ranker_annually=ranker_annually, 
        ranker_monthly=ranker_monthly, 
        ranker_weekly=ranker_weekly, 
        data=data, 
        modes=modes, 
        categories=categories, 
        options=options
    )


# Render customization of quiz.
@app.route("/customize", methods=["GET", "POST"])
def customize():
    # If a request was submitted as POST, record the input data and redirect to quiz page.
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
    
    # If it's a GET request, display possible customizations for the quiz.
    mode = ["Capital city", "Country"]
    category = ["Earth", "Asia", "Africa", "North America", "South America", "Europe", "Australia"]
    option = ["True or False", "Multiple Choice", "Identification"]

    return render_template("customize.html", modes=mode, categories=category, options=option)


# Generate the quiz based on mode and category
@app.route("/quiz", methods=["GET"])
def quiz():
    # Retrieve values from session.
    mode = session.get('mode')  
    category = session.get('category') 
    option = session.get('option') 

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    if category == "Earth":
        query = cursor.execute('select id, country, capital, continent from countries')
    else:
        query = cursor.execute('select id, country, capital, continent from countries where continent = ?', (category,))

    result = query.fetchall()

    connection.commit()
    connection.close()

    # Convert elements from result to a Country objects.
    countries = [Country(*row) for row in result]
    random.shuffle(countries)


    # First ten countries in the list will serve as the questions.
    questions = []
    for i in range(10): 
        if option == "True or False":
            # If answer is false, find some other country/capital to use for the question.
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

    # Record the starting time of user in taking the quiz.
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
    
    datetime_start = session.get('datetime_start').replace(tzinfo=None)

    datetime_end = datetime.now().replace(tzinfo=None)
    session['datetime_end'] = datetime_end

    duration = int((datetime_end - datetime_start).total_seconds())

    # Convert questions_data back to its Class. 
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

    # Check if each input matches its answer key.
    score = 0
    for i in range(10):
        answer = request.form.get(str(questions[i].id)) or "None"
        questions[i].answer = answer

        if (questions[i].answer == questions[i].answer_key):
            score += 1

    return render_template("score.html", mode=mode, category=category, option=option, score=score, duration=duration, questions=questions)


@app.route("/upload", methods=["POST"])
def upload():
    mode = session.get('mode')  
    if mode == "name":
        mode = "country"

    category = session.get('category') 
    option = session.get('option') 
    duration = session.get('datetime_end').replace(tzinfo=None) - session.get('datetime_start').replace(tzinfo=None)

    user = request.form.get("username")
    score = int(request.form.get("score"))

    # Get the date when the quiz was taken in a YYYY-MM-DD format.
    record_date = datetime.now().strftime("%Y-%m-%d")

    # Each item in true or false is worth 2 points.
    # Each item in multiple choice is worth 3 points.
    # Each item in identification is worth 5 points.
    score_multiplier = {
        "True or False": 2,
        "Multiple Choice": 3,
        "Identification": 5
    }
    score *= score_multiplier.get(option, 1)

    # Upload results to database.
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO highscore(user, score, mode, category, option, duration, record_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user, score, mode, category, option, duration, record_date)
    )
    connection.commit()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)