package com.gestion.ecole.ui.menu.InformationsEleve;

public class ItemDesciplineEleve {
    String tvNomMatiere,tvDateHeure,tvStatus;

    public ItemDesciplineEleve(String tvNomMatiere,String tvDateHeure,String tvStatus){
        this.tvNomMatiere=tvNomMatiere;
        this.tvDateHeure=tvDateHeure;
        this.tvStatus=tvStatus;
    }


    public String getNomMatiere() {
        return tvNomMatiere;
    }

    public String getDateHeure() {
        return  tvDateHeure;
    }

    public  String getSatus(){ return tvStatus;}
}
