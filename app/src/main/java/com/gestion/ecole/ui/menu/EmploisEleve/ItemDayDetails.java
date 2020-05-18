package com.gestion.ecole.ui.menu.EmploisEleve;

public class ItemDayDetails {
    String subject,time,tvTeacher;

    public ItemDayDetails(String subject,String time,String tvTeacher){
        this.subject=subject;
        this.time=time;
        this.tvTeacher=tvTeacher;
    }

    public String getSubject(){return  subject;}

    public String getTime(){return  time;}

    public String getTeacher(){return tvTeacher;}

}
