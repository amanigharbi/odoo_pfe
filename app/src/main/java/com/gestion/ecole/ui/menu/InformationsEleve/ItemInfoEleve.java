package com.gestion.ecole.ui.menu.InformationsEleve;

public class ItemInfoEleve {
    String tvNom,tvPrenom,tvNomParent,tvNomClasse;

    public ItemInfoEleve(String tvNom,String tvNomParent,String tvNomClasse){
        this.tvNom=tvNom;
      //  this.tvPrenom=tvPrenom;
        this.tvNomParent=tvNomParent;
        this.tvNomClasse=tvNomClasse;
    }

    public String getNom() {
        return tvNom;
    }

    public String getPrenom() {
        return tvPrenom;
    }


    public String getNomParent() {
        return  tvNomParent;
    }

    public  String getNomClasse(){ return tvNomClasse;}
}
