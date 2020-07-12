package com.gestion.ecole.ui.menu.ContactEnseignant;

public class ItemEnseignant {
String tvNomPrenom,tvEmail,tvNum,tvMatiere;

public ItemEnseignant(String tvNP, String tvE,String tvNum){
    this.tvNomPrenom= tvNP;
    this.tvEmail=tvE;
    this.tvNum=tvNum;

}

    public String getNomPrenom() {
        return tvNomPrenom;
    }


    public String getEmail() {
        return  tvEmail;
    }

    public  String getNum(){ return tvNum;}



}
