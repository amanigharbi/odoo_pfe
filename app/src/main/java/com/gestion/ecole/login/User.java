package com.gestion.ecole.login;

public class User {
    String mdp;
    String email,id,name_parent,db,url,idResUsers;

    public User(String email,String mdp,String idResUsers,String id,String name_parent,String db,String url) {

        this.email = email;
        this.mdp = mdp;
        this.idResUsers=idResUsers;
        this.id = id;
        this.name_parent = name_parent;
        this.db=db;
        this.url=url;

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

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName_parent() {
        return name_parent;
    }

    public void setName_parent(String name_parent) {
        this.name_parent = name_parent;
    }

    public String getDb() {
        return db;
    }

    public void setDb(String db) {
        this.db = db;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getIdResUsers() {
        return idResUsers;
    }

    public void setIdResUsers(String idResUsers) {
        this.idResUsers = idResUsers;
    }
}


