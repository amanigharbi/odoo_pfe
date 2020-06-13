package com.gestion.ecole.login;

public class User {
    String mdp;
    String email;

    public User(String email,String mdp) {
        this.mdp = mdp;
        this.email = email;
    }

    public String getmdp() {
        return mdp;
    }

    public void setmdp(String mdp) {
        this.mdp = mdp;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
