package com.gestion.ecole.ui.notif;

public class ItemNotification {
    String titre,notif_message;

   public ItemNotification(String titre,String notif_message){
        this.titre=titre;
        this.notif_message=notif_message;
    }

    public String getTitreNotif() {
        return  titre;
    }

    public  String getNotif_message(){ return notif_message;}
}
