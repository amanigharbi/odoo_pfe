package com.gestion.ecole.ui.notif;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import com.gestion.ecole.R;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetConnectionData;
import com.gestion.ecole.odoo.SetDataOdoo;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class NotifActivity extends AppCompatActivity {
    AsyncTask<URL, String, Boolean> setnotif;
RecyclerView rvNotification;
    ArrayList<ItemNotification> itemNotification;

    ArrayList<String> titre=new ArrayList<>();
    ArrayList<String> notifMessage=new ArrayList<>();

    String[] titreArray,notifMessageArray;

    AdapterNotification NotifAdapter;
    String parentID;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.notif_activity);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        rvNotification = findViewById(R.id.rvNotification);
        rvNotification.setHasFixedSize(true);


        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(NotifActivity.this);
        rvNotification.setLayoutManager(layoutManager);

        SessionManagement sessionManagement = new SessionManagement(NotifActivity.this);
        parentID = sessionManagement.getId();
        String db=sessionManagement.getSESSION_DB();
        String url=sessionManagement.getSESSION_URL();
        String mdp=sessionManagement.getMdp();
        String res_users=sessionManagement.getSESSION_RES_USERS();

        try {

            // id eleve du table student.student
            AsyncTask<URL, String, List> InfoEleve = new GetConditionData(db,url,mdp,res_users,"student.student", new String[]{"id", "last", "name", "parent_id",
                    "standard_id", "parent_id"}, "parent_id.id", parentID).execute();
            List ListInfoEleve = InfoEleve.get();
            for (Map<String, Object> item1 : (List<Map<String, Object>>) ListInfoEleve) {

                //Associer l'id de l'élève avec id_eleve du table history.notification avec tous les etat du message
                AsyncTask<URL, String, List> notif = new GetConditionData(db,url,mdp,res_users,"history.notification",
                        new String[]{"title", "message", "status_message", "student_id", "id"}, "student_id.id", item1.get("id").toString()).execute();


                List ListNotif = notif.get();

                for (Map<String, Object> item : (List<Map<String, Object>>) ListNotif) {

                    //Ajouter les attributs dans array
                    titre.add("Notification De " + item.get("title").toString());
                    notifMessage.add(item.get("message").toString());

                    //lors de louverture du notification or les historiques, l'état du message va etre modifier à "Sent"
                    setnotif = new SetDataOdoo("history.notification", item.get("id").toString(),
                            "status_message", "Sent").execute();
                    System.out.println("notif"+setnotif.get());
                }
            }

        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        titreArray = titre.toArray(new String[titre.size()]);
        notifMessageArray = notifMessage.toArray(new String[notifMessage.size()]);

        itemNotification = new ArrayList<>();
        for (int i = 0; i < titreArray.length; i++) {
            itemNotification.add(new ItemNotification(
                    titreArray[i].toString(),
                    notifMessageArray[i].toString()
            ));
        }

        NotifAdapter = new AdapterNotification(itemNotification, NotifActivity.this);
        rvNotification.setAdapter(NotifAdapter);
        rvNotification.getAdapter().notifyDataSetChanged();
        rvNotification.scheduleLayoutAnimation();


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu){
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;

    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id= item.getItemId();
        if (id== R.id.deconnexion){
            SessionManagement sessionManagement = new SessionManagement(NotifActivity.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }}