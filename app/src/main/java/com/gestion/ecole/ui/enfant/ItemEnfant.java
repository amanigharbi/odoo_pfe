package com.gestion.ecole.ui.enfant;

public class ItemEnfant {
    String tvNom,tvNomParent,tvNomClasse,idEnfant;

    public ItemEnfant(String tvNom,String tvNomParent,String tvNomClasse,String idEnfant
    ){
        this.tvNom=tvNom;
        this.tvNomParent=tvNomParent;
        this.tvNomClasse=tvNomClasse;
        this.idEnfant=idEnfant;

    }

    public String getNom() {
        return tvNom;
    }

    public String getNomParent() {
        return  tvNomParent;
    }

    public  String getNomClasse(){ return tvNomClasse;}
    public  String getIdEnfant(){ return idEnfant;}
}
