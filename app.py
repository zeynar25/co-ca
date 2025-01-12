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

    # change this part SQL team, retrive niyo entries where continent = category,
    # tas convert niyo to a list of Country then assign sa countries.
    ph = Country("Philippines", "Manila", "Asia")
    jp = Country("Japan", "Tokyo", "Asia")
    sk = Country("South Korea", "Seoul", "Asia")
    nk = Country("North Korea", "Pyeongyang", "Asia")
    ch = Country("China", "Beijing", "Asia")
    countries = [ph, jp, sk, nk, ch]

    # Generate 3 questions.
    while len(questions) < 3:
        curr = random.choice(countries)

        # Check in curr already exist as a question
        skip = False
        for q in questions :
            if q.name == curr.name:
                skip = True
                break

        if skip:
            continue

        question = Question(curr.name, curr.capital, curr.continent)

        if mode == "capitals":
            question.add_option(curr.capital)
            while len(question.options) < 3:
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
            while len(question.options) < 3:
                curr2 = random.choice(countries)

                # Skip when curr2.capital already exist in option.
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

    return render_template('quiz.html', mode=mode, category=category, questions=questions)



# Unimplemented functions.

# Check the quiz, and upload the score to highscore db.
@app.route("/submit", methods=["POST"])
def check():
    ...

# Display highscore.
# Can be filtered by category.
@app.route("/highscore", methods=["GET"])
def highscore():
    ...

if __name__ == "__main__":
    app.run(debug=True)