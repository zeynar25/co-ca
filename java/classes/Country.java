package classes;

public class Country {
    private int id;
    private String name;
    private String capital;

    // Constructor
    public Country(int id, String name, String capital) {
        setId(id);
        setName(name);
        setCapital(capital);
    }

    // Getter and Setter for id
    public int getId() {
        return id;
    }

    public void setId(int id) {
        if (id > 0) {
            this.id = id;
        } else {
            throw new IllegalArgumentException("Invalid ID");
        }
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = capitalize(name);
        } else {
            throw new IllegalArgumentException("Invalid country name");
        }
    }

    public String getCapital() {
        return capital;
    }

    public void setCapital(String capital) {
        if (capital != null && !capital.trim().isEmpty()) {
            this.capital = capitalize(capital);
        } else {
            throw new IllegalArgumentException("Invalid capital name");
        }
    }
    
    private String capitalize(String input) {
        if (input == null || input.isEmpty()) {
            return input;
        }
        return input.substring(0, 1).toUpperCase() + input.substring(1).toLowerCase();
    }

    // Override toString
    @Override
    public String toString() {
        return "Country: " + name + ", Capital: " + capital;
    }
}

