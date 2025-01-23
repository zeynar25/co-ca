import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

import classes.Country;
import classes.Question;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Country> countries = new ArrayList<>();
        Country ph = new Country(1, "Philippines", "Manila");
        Country jp = new Country(2, "Japan", "Tokyo");
        Country sk = new Country(3, "South Korea", "Seoul");
        Country nk = new Country(4, "North Korea", "Pyongyang");
        Country ch = new Country(5, "China", "Beijing");

        countries.add(ph);
        countries.add(jp);
        countries.add(sk);
        countries.add(nk);
        countries.add(ch);

        boolean loop = true;
        while (loop) {
            System.out.println("Welcome to Co-Ca");
            System.out.println("[1] Play");
            System.out.println("[2] About");
            System.out.println("[3] Exit");

            int answer = 0;
            try{
                System.out.print("Command: ");
                answer = input.nextInt();
                input.nextLine();
            } catch(Exception e) {
                input.nextLine();
                System.out.println("input command must be a number from 1 to 3");
                continue;
            }

            switch (answer) {
                case 1:
                    System.out.println();
                    quiz(input, countries);
                    break;
                case 2:
                    about();
                    break;
                case 3:
                    loop = false;
                    break;
            
                default:
                    System.out.println("input must be a number from 1 to 3");
                    break;
            }

            System.out.println();
        }
        System.out.println("Thank you for playing<3");
    }

    public static void quiz(Scanner input, ArrayList<Country> countries) {
        Collections.shuffle(countries);
        ArrayList<Question> questions = new ArrayList<>();

        for (int i = 0; i < 3; i++) {
            String answerKey = null;
            String description = "What is the capital of " + countries.get(i).getName() + "?";
            answerKey = countries.get(i).getCapital();

            Question question = new Question(
                countries.get(i).getId(),
                countries.get(i).getName(),
                countries.get(i).getCapital(),
                description,
                answerKey
            );

            question.addOptions(countries);
            questions.add(question);
        }

        int score = 0;
        for (Question q : questions) {
            System.out.println(q.getQuestion()); 
            for (String choice : q.getOptions()) {
                System.out.println("- " + choice);
            }

            System.out.print("Which country: ");
            q.setAnswer(input.nextLine().trim());

            if (q.getAnswer().toLowerCase().equals(q.getAnswerKey().toLowerCase())) {
                score++;
            }
            System.out.println();
        }

        if (score <= 1) {
            System.out.println("Congratulations! You got " + score + " item right!\n");
        } else {
            System.out.println("Congratulations! You got " + score + " items right!\n");
        }
        
        for (Question q : questions) {
            System.out.println(q.getQuestion()); 
            System.out.println("Your answer: " + q.getAnswer());
            System.out.println("Correct answer: " + q.getAnswerKey());
            System.out.println();
        }
    }

    public static void about() {
        System.out.println();
        System.out.println("About Co-Ca");
        System.out.println("At Co-Ca, our mission is simple yet impactful: to help people across the globe become more familiar with countries, their capital cities, and their rich cultures.");
        System.out.println("We believe that understanding geography is more than just memorizing maps and names; it’s a way to appreciate the diversity and uniqueness of our shared world.");
        System.out.println();
    
        System.out.println("Why Co-Ca?");
        System.out.println("The world is a vast and beautiful place, home to different nations, cultures, traditions, and histories.");
        System.out.println("By learning about countries and their capitals, we take the first step toward understanding and respecting the unique identities that make each country special.");
        System.out.println("Co-Ca isn’t just a quiz platform; it’s a bridge to global awareness.");
        System.out.println();
        System.out.println("Fostering Respect for Cultures:");
        System.out.println("At its core, Co-Ca is about more than just knowledge—it’s about building respect.");
        System.out.println("By learning about a country's capital city and its place on the map, you gain insights into its culture, people, and way of life.");
        System.out.println("These small steps can lead to a more connected and compassionate global community.");
        System.out.println();
        System.out.println("Testing and Expanding Your Knowledge:");
        System.out.println("Think you know all the capital cities in the world? Or perhaps you want to challenge yourself?");
        System.out.println("Co-Ca is here to test your knowledge and push your boundaries.");
        System.out.println("Whether you’re a geography enthusiast, a curious learner, or someone preparing for an important quiz or competition, Co-Ca offers a fun and interactive way to learn.");
        System.out.println();
        System.out.println("Making Learning Fun and Interactive:");
        System.out.println("Geography can sometimes feel overwhelming, but Co-Ca makes it engaging through gamified learning.");
        System.out.println("Answer questions, test your memory, and track your progress—all while having fun!");
        System.out.println("With challenges ranging from identifying capital cities to matching countries, there’s always something new to learn and enjoy.");
        System.out.println();
    
        System.out.println("Our Vision");
        System.out.println("We envision a world where learning about geography and cultures becomes second nature—where understanding each other’s differences fosters unity rather than division.");
        System.out.println("Co-Ca aims to empower individuals with knowledge and the ability to connect with people from all walks of life.");
        System.out.println();
    
        System.out.println("How Does It Work?");
        System.out.println("- Learn Through Quizzes: Answer questions about countries and their capitals in various formats, including multiple-choice, true or false, and identification.");
        System.out.println("- Track Your Progress: Keep track of your scores and see how your knowledge improves over time.");
        System.out.println("- Respect and Curiosity: Beyond facts and figures, learn the deeper significance of each country and its culture.");
        System.out.println();
    
        System.out.println("Join Us on This Journey");
        System.out.println("Whether you’re a student, a trivia enthusiast, or someone who simply loves exploring the world, Co-Ca welcomes you.");
        System.out.println("Together, let’s discover the wonders of the globe, one country and one capital at a time.");
        System.out.println();
        System.out.println("Explore. Learn. Respect.");
        System.out.println("Welcome to Co-Ca!");
    }    
}
