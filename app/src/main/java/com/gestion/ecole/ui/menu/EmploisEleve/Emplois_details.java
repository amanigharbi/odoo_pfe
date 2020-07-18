package com.gestion.ecole.ui.menu.EmploisEleve;

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
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.odoo.DeleteRegIdOdoo;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetConditionData;
import com.google.firebase.iid.FirebaseInstanceId;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class Emplois_details extends AppCompatActivity {
    RecyclerView rvDayDetails;

    AdapterDayDetails ddAdapter;

    ArrayList<ItemDayDetails> itemDayDetails;

    ArrayList<String> subject = new ArrayList<>();
    ArrayList<String> time = new ArrayList<>();
    ArrayList<String> teacher = new ArrayList<>();
    String res_users,db,url,mdp,intentId, parentID,id_reg;
    String[] subjectArray, timeArray,teacherArray;

    AsyncTask<URL, String, List> monday, tuesday, wednesday, thursday, friday, saturday;
    List listmonday, listtuesday, listwednesday, listthursday, listfriday, listsaturday;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emplois_details);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        rvDayDetails = findViewById(R.id.rvDayDetails);
        rvDayDetails.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(Emplois_details.this);
        rvDayDetails.setLayoutManager(layoutManager);

        SessionManagement sessionManagement = new SessionManagement(Emplois_details.this);
         res_users=sessionManagement.getSESSION_RES_USERS();
         db=sessionManagement.getSESSION_DB();
        url=sessionManagement.getSESSION_URL();
        mdp=sessionManagement.getMdp();

        try {
            Intent intent=getIntent();
            String intentId=intent.getStringExtra("idEnfant");
            //Extraire id du classe du table student.student
            AsyncTask<URL, String, List> standard_eleve = new GetConditionData(db,url,mdp,res_users,"student.student",
                    new String[]{"id","standard_id", "school_id"},"id",intentId).execute();
            List stan = standard_eleve.get();


            for (Map<String, Object> item0 : (List<Map<String, Object>>) stan) {
                Object[] standard = (Object[]) item0.get("standard_id");
                Object[] school = (Object[]) item0.get("school_id");

                //Asocier id du classe du table  student.student avec table time.table
                AsyncTask<URL, String, List> emploie = new Get2ConditionData(db,url,mdp,res_users,"time.table", new String[]{"id", "standard_id", "school_id"},
                        "standard_id.id", standard[0].toString(), "school_id.id", school[0].toString()).execute();

                List emploie_id = emploie.get();

                //Associer id d'emploie du table time.table avec table time.table.line
                for (Map<String, Object> item1 : (List<Map<String, Object>>) emploie_id) {
                    monday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Monday").execute();
                    listmonday = monday.get();

                    tuesday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Tuesday").execute();
                    listtuesday = tuesday.get();

                    wednesday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Wednesday").execute();
                    listwednesday = wednesday.get();

                    thursday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Thursday").execute();
                    listthursday = thursday.get();

                    friday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Friday").execute();
                    listfriday = friday.get();

                    saturday = new Get2ConditionData(db,url,mdp,res_users,"time.table.line", new String[]{"start_time", "end_time", "subject_id", "week_day", "table_id","teacher_id"},
                            "table_id.id", item1.get("id").toString(), "week_day", "Saturday").execute();
                    listsaturday = saturday.get();

                    //Associer le jour selectionné de l'activity_emploie_day avec les données necessaires de chaque jour
                    String selected_day = EmploisEleve.sharedPreferences.getString(EmploisEleve.SEL_DAY, null);

                    if (selected_day.equalsIgnoreCase("Monday")) {


                        for (Map<String, Object> item : (List<Map<String, Object>>) listmonday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));
                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());
                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }


                    } else if (selected_day.equalsIgnoreCase("Tuesday")) {
                        for (Map<String, Object> item : (List<Map<String, Object>>) listtuesday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));

                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());

                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }

                    } else if (selected_day.equalsIgnoreCase("Wednesday")) {
                        for (Map<String, Object> item : (List<Map<String, Object>>) listwednesday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));

                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());

                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }

                    } else if (selected_day.equalsIgnoreCase("Thursday")) {
                        for (Map<String, Object> item : (List<Map<String, Object>>) listthursday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));

                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());

                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }

                    } else if (selected_day.equalsIgnoreCase("Friday")) {
                        for (Map<String, Object> item : (List<Map<String, Object>>) listfriday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));

                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());

                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }

                    } else {
                        for (Map<String, Object> item : (List<Map<String, Object>>) listsaturday) {
                            time.add((item.get("start_time").toString()+" - "+item.get("end_time").toString()));

                            Object[] sub = (Object[]) item.get(("subject_id"));
                            subject.add(sub[1].toString());

                            Object[] teach = (Object[]) item.get(("teacher_id"));
                            teacher.add(teach[1].toString());
                        }
                    }


                }
            }
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        timeArray = time.toArray(new String[time.size()]);
        subjectArray = subject.toArray(new String[subject.size()]);
        teacherArray = teacher.toArray(new String[teacher.size()]);

        itemDayDetails=new ArrayList<>();
        for(int i=0;i<subjectArray.length;i++) {

            itemDayDetails.add(new ItemDayDetails(subjectArray[i].toString(),
                    timeArray[i].toString(),
                    teacherArray[i].toString()));}

        ddAdapter = new AdapterDayDetails(itemDayDetails,Emplois_details.this);
        rvDayDetails.setAdapter( ddAdapter);
        rvDayDetails.getAdapter().notifyDataSetChanged();
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
            String registration_id = FirebaseInstanceId.getInstance().getToken();
            AsyncTask<URL, String, List> regMobile  = new Get2ConditionData(db,url,mdp,res_users,"parent.registration", new String[]{"id","reg_id", "parent_id"},
                    "parent_id.id", parentID,"reg_id",registration_id).execute();

            try {

                List regMobileList=regMobile.get();
                for (Map<String, Object> item5 : (List<Map<String, Object>>) regMobileList) {
                    id_reg=item5.get("id").toString();
                }
                //Supprimer le registration id du parent
                AsyncTask<URL, String, Boolean> delete  = new DeleteRegIdOdoo(db,url,mdp,res_users,"parent.registration", id_reg).execute();

            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            // Supprimer la session du parent
            // Redirect parent dans la page du login
            SessionManagement sessionManagement = new SessionManagement(Emplois_details.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }



}