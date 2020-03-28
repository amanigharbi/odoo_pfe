package com.gestion.ecole;

public class ScreenItem {

    String textIntro,descIntro;
    int imgIntro;

    public ScreenItem(String title, String desc,int screenImg) {
        textIntro = title;
        descIntro = desc;
        imgIntro = screenImg;
    }
    public ScreenItem( int screenImg) {


        imgIntro = screenImg;
    }

    public void setTitle(String title) {
        textIntro = title;
    }


    public void setScreenImg(int screenImg) {
        imgIntro = screenImg;
    }

    public String getTitle() {
        return textIntro;
    }


    public int getScreenImg() {
        return imgIntro;
    }

    public  String getDescription(){ return descIntro;}
}
