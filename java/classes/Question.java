package classes;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public class Question extends Country {
    private String question;
    private String answerKey;
    private ArrayList<String> options;
    private String answer;

    public Question(int id, String name, String capital, String question, String answerKey) {
        super(id, name, capital);
        this.question = question;
        this.answerKey = answerKey;
        this.options = new ArrayList<>();
        this.answer = null;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getAnswerKey() {
        return answerKey;
    }

    public void setAnswerKey(String answerKey) {
        this.answerKey = answerKey;
    }

    public ArrayList<String> getOptions() {
        return options;
    }

    public void setOptions(ArrayList<String> options) {
        if (options != null) {
            this.options = options;
        } else {
            throw new IllegalArgumentException("Options must be a list");
        }
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer != null ? answer.trim() : null;
    }

    @Override
    public String toString() {
        return super.toString() + ", Question: " + question + ", Answer Key: " + answerKey;
    }

    public void addOptions(ArrayList<Country> countries) {
        Set<String> optionsSet = new HashSet<>();
        optionsSet.add(this.getCapital());

        Random random = new Random();
        while (optionsSet.size() < 4) {
            Country randomCountry = countries.get(random.nextInt(countries.size()));
            String randomOption = randomCountry.getCapital();
            optionsSet.add(randomOption);
        }

        this.options = new ArrayList<>(optionsSet);
        Collections.shuffle(this.options);
    }
}