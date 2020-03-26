package com.gestion.ecole.ui.menu;

public class ItemMenu {
    String tvTitle,tvDesc;
    int imgArticle;

    public ItemMenu(String title,String desc,Integer img){
        tvTitle=title;
        tvDesc=desc;
        imgArticle=img;

    }
    public String getTitle() {
        return tvTitle;
    }


    public int getScreenImg() {
        return imgArticle;
    }

    public  String getDescription(){ return tvDesc;}
}
