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

def seconds_to_time(total_seconds):
    # Convert total seconds to hours, minutes, seconds, and milliseconds
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 1000)

    # Format as hh:mm:ss.mmm
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:05}"
    return formatted_time

def get_month_name(month_number):
    # List of month names
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Check if the input is valid
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number. Please enter a number between 1 and 12."

# Landing page: displays play and highscore button.
@app.route("/", methods=["GET", "POST"])
def index():
    # Filter choices.
    modes = ["All", "Capital city", "Country"]
    categories = ["All", "Earth", "Asia", "Africa", "North America", "South America", "Europe", "Australia"]
    options = ["All", "True or False", "Multiple Choice", "Identification"]
    
    year = datetime.now().year
    month = get_month_name(datetime.now().month)

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

        # Set default values if 'All' is selected
        where_conditions = []
        params = []

        # Filter by mode
        if mode != "All":
            where_conditions.append("mode = ?")
            params.append(mode)

        # Filter by category
        if category != "All":
            where_conditions.append("category = ?")
            params.append(category)

        # Filter by option
        if option != "All":
            where_conditions.append("option = ?")
            params.append(option)


        query = '''SELECT id, user, score, mode, category, option, duration, record_date 
            FROM highscore'''

        # Make 5 copies of query
        query_all = query
        query_annually = query
        query_monthly = query
        query_weekly = query

        # Add WHERE clause if there are any filters
        if where_conditions:
            query_all += " WHERE " + " AND ".join(where_conditions)
            query_annually += " WHERE " + " AND ".join(where_conditions)
            query_monthly += " WHERE " + " AND ".join(where_conditions)
            query_weekly += " WHERE " + " AND ".join(where_conditions)

        # Add ORDER BY and LIMIT
        query_all += " ORDER BY score DESC, duration LIMIT 100"
        query_annually += " ORDER BY score DESC, duration LIMIT 50"
        query_monthly += " ORDER BY score DESC, duration LIMIT 25"
        query_weekly += " ORDER BY score DESC, duration LIMIT 10"


        # Fetch results and store in a list.
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(query_all, params)
        result_all = cursor.fetchall()

        cursor.execute(query_annually, params)
        result_annually = cursor.fetchall()

        cursor.execute(query_monthly, params)
        result_monthly = cursor.fetchall()

        cursor.execute(query_weekly, params)
        result_weekly = cursor.fetchall()

        connection.close()

        # Convert each fetched duration (in seconds) to HH:MM:SS.sssss format
        result_all = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_all]

        result_annually = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_annually]

        result_monthly = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_monthly]

        result_weekly = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_weekly]

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
            options=options,
            month=month,
            year=year
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

    result_all = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_all]

    result_annually = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_annually]

    result_monthly = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_monthly]

    result_weekly = [(row[0], row[1], row[2], row[3], row[4], row[5], seconds_to_time(row[6]), row[7]) for row in result_weekly]

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
        options=options,
        month=month,
        year=year
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

    duration = datetime_end - datetime_start
    duration = duration.total_seconds()
    session['duration'] = duration

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

        if (questions[i].answer.upper() == questions[i].answer_key.upper()):
            score += 1
            questions[i].state = True

    return render_template("score.html", mode=mode, category=category, option=option, score=score, duration=seconds_to_time(duration), questions=questions)


@app.route("/upload", methods=["POST"])
def upload():
    mode = session.get('mode')  
    if mode == "name":
        mode = "country"

    category = session.get('category') 
    option = session.get('option') 
    duration = session.get('duration') 

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

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)