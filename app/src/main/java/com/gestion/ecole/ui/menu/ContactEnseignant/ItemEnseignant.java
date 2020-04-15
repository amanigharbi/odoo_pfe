package com.gestion.ecole.ui.menu.ContactEnseignant;

public class ItemEnseignant {
String tvNomPrenom,tvEmail,tvNum;

public ItemEnseignant(String tvNP, String tvE,String tvN){
    tvNomPrenom= tvNP;
    tvEmail=tvE;
    tvNum=tvN;
}

    public String getNomPrenom() {
        return tvNomPrenom;
    }


    public String getEmail() {
        return  tvEmail;
    }

    public  String getNum(){ return tvNum;}

}
