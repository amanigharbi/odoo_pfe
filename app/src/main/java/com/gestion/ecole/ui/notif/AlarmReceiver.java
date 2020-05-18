package com.gestion.ecole.ui.notif;

import android.annotation.SuppressLint;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.SystemClock;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.core.app.NotificationCompat;

import com.gestion.ecole.R;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetDataOdoo;

import static android.app.NotificationManager.IMPORTANCE_DEFAULT;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class AlarmReceiver extends BroadcastReceiver {
    private static final String CHANNEL_ID = "com.notification.ecole";


    ArrayList<String> title=new ArrayList<>();
    ArrayList<String> message=new ArrayList<>();
    String[] titleArray,messageArray;

    Notification notification;
    Notification.Builder builder;

    @SuppressLint({"WrongConstant", "NewApi"})
    @RequiresApi(api = Build.VERSION_CODES.JELLY_BEAN)
    @Override
    public void onReceive(Context context, Intent intent) {

        //notification
        Intent notificationIntent = new Intent(context, NotifActivity.class);

        TaskStackBuilder stackBuilder = TaskStackBuilder.create(context);
        stackBuilder.addParentStack(NotifActivity.class);
        stackBuilder.addNextIntent(notificationIntent);

        PendingIntent pendingIntent = stackBuilder.getPendingIntent(0, PendingIntent.FLAG_UPDATE_CURRENT);


        try {
            // id eleve du table student.student
        AsyncTask<URL, String, List> InfoEleve = new GetDataOdoo("student.student", new String[]{"id"}).execute();
        List ListInfoEleve = InfoEleve.get();
        for (Map<String, Object> item1 : (List<Map<String, Object>>) ListInfoEleve) {


            //Associer l'id de l'élève avec id_eleve du table history.notification et avec condition status_message = In Progress
        AsyncTask<URL, String, List> notif = new Get2ConditionData("history.notification",
                new String[]{"title", "message","status_message","student_id"},"student_id.id",item1.get("id").toString(),"status_message","In Progress").execute();


            List ListNotif = notif.get();

            //s'il n'y a aucune notification l'application continue à executer les autres instructions
            if (ListNotif.equals("")) {
                Toast.makeText(context, "aucune notification", Toast.LENGTH_LONG).show();
                System.out.println("aucune notification");
            } else {

             //sinon il va afficher la notification nécessaire dans le table
            for(Map<String,Object> item : (List<Map<String,Object>>) ListNotif) {

                //Ajouter les attributs dans array
                title.add(item.get("title").toString());
                message.add(item.get("message").toString());

            }
        }}
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        titleArray = title.toArray(new String[title.size()]);
        messageArray = message.toArray(new String[message.size()]);


        for(int i=0;i<titleArray.length;i++) {

             builder = new Notification.Builder(context);

             //creer la notifaction avec les messages et icon ..
            notification = builder.setContentTitle(titleArray[i].toString())
                    .setContentText(messageArray[i].toString())
                    .setTicker("New Message Alert!")
                    .setSmallIcon(R.drawable.ecoleicon)
                    .setPriority(NotificationCompat.PRIORITY_HIGH)
                    .setCategory(NotificationCompat.CATEGORY_MESSAGE)
                    .setAutoCancel(true)
                    //attribuer cette notification à l'intent
                    .setContentIntent(pendingIntent).build();




        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder.setChannelId(CHANNEL_ID);
        }

        NotificationManager notificationManager = (NotificationManager) context.getSystemService(context.NOTIFICATION_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "Notification école",
                    IMPORTANCE_DEFAULT
            );
            notificationManager.createNotificationChannel(channel);
        }
       //mettre 2000 mn entre chaque notification
        SystemClock.sleep(2000);
        //start notification
        notificationManager.notify(i, notification);


    }}
}
