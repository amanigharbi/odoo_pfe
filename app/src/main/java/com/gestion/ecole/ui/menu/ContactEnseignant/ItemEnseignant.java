package com.gestion.ecole.ui.menu.ContactEnseignant;

public class ItemEnseignant {
String tvNomPrenom,tvEmail,tvNum,tvMatiere;

public ItemEnseignant(String tvNP, String tvE,String tvNum,String tvMatiere){
    this.tvNomPrenom= tvNP;
    this.tvEmail=tvE;
    this.tvNum=tvNum;
    this.tvMatiere=tvMatiere;
}

    public String getNomPrenom() {
        return tvNomPrenom;
    }


    public String getEmail() {
        return  tvEmail;
    }

    public  String getNum(){ return tvNum;}

    public  String getMatiere(){ return tvMatiere;}

}
