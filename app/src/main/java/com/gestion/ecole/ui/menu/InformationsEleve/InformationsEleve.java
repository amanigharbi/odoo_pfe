package com.gestion.ecole.ui.menu.InformationsEleve;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.odoo.GetConditionData;


import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class InformationsEleve extends AppCompatActivity {

    CardView cvImage;

    RecyclerView rvSanctionsEleve,rvDesciplineEleve,rvAbscenceJournaliaireEleve;
    AdapterSanctionsEleve mAdapter;
    AdapterDesciplineEleve DescAdapter;
    AdapterDiscJourEleve discJourAdapter;

    ArrayList<ItemSanctionsEleve> itemSanctionsEleve;
    ArrayList<ItemDesciplineEleve> itemDesciplineEleve;
    ArrayList<ItemDiscJourEleve>itemDiscJourEleves;

    ArrayList<String> sanctions=new ArrayList<>();
    ArrayList<String> nombre=new ArrayList<>();

    ArrayList<String> nomMatiere=new ArrayList<>();
    ArrayList<String> dateHeure=new ArrayList<>();
    ArrayList<String> status=new ArrayList<>();

    ArrayList<String> statusDisc=new ArrayList<>();
    ArrayList<String> date=new ArrayList<>();

    String[] sanctionArray,nombreArray,nomMatiereArray,dateHeureArray,statusArray,statusDiscArray,dateArray;

    String id,parentID;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_informations_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        cvImage= findViewById(R.id.cvImage);

        rvSanctionsEleve=findViewById(R.id.rvSanctionsEleve);
        rvSanctionsEleve.setHasFixedSize(true);

        rvDesciplineEleve=findViewById(R.id.rvDesciplineEleve);
        rvDesciplineEleve.setHasFixedSize(true);

        rvAbscenceJournaliaireEleve=findViewById(R.id.rvAbscenceJournaliaireEleve);
        rvAbscenceJournaliaireEleve.setHasFixedSize(true);


        cvImage.scheduleLayoutAnimation();
      //  cvInfo.scheduleLayoutAnimation();

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InformationsEleve.this);
        RecyclerView.LayoutManager layoutManager2 = new LinearLayoutManager(InformationsEleve.this);
        RecyclerView.LayoutManager layoutManager3 = new LinearLayoutManager(InformationsEleve.this);
        rvSanctionsEleve.setLayoutManager(layoutManager);
       rvDesciplineEleve.setLayoutManager(layoutManager2);
        rvAbscenceJournaliaireEleve.setLayoutManager(layoutManager3);

        SessionManagement sessionManagement = new SessionManagement(InformationsEleve.this);
        String res_users=sessionManagement.getSESSION_RES_USERS();
        String db=sessionManagement.getSESSION_DB();
        String url=sessionManagement.getSESSION_URL();
        String mdp=sessionManagement.getMdp();

        try {

            Intent intent=getIntent();
            String intentId=intent.getStringExtra("id");

                //Informations Discipline
                AsyncTask<URL, String, List> infoDescipline = new GetConditionData(db,url,mdp,res_users,"student.desciplines", new String[]{"student_id", "subject_id", "device_datetime", "status"},
                        "student_id.id", intentId).execute();

                AsyncTask<URL, String, List> infoSanctions = new GetConditionData(db,url,mdp,res_users,"student.sanctions", new String[]{"student_id", "sanction", "number"},
                        "student_id.id", intentId).execute();

            AsyncTask<URL, String, List> infoDiscJour = new GetConditionData(db,url,mdp,res_users,"student.daily.disciplines", new String[]{"student_id", "status", "date"},
                    "student_id.id", intentId).execute();

                List ListInfoDescipline = infoDescipline.get();
                List ListInfoSanctions = infoSanctions.get();
                List ListInfoDiscJour = infoDiscJour.get();


                for (Map<String, Object> item5 : (List<Map<String, Object>>) ListInfoDescipline) {

                    Object[] mat = (Object[]) item5.get("subject_id");
                    nomMatiere.add(mat[1].toString());

                    dateHeure.add(item5.get("device_datetime").toString());
                    status.add(item5.get("status").toString());
                }
                for (Map<String, Object> item : (List<Map<String, Object>>) ListInfoSanctions) {

                    sanctions.add(item.get("sanction").toString());
                    nombre.add(item.get("number").toString());
                }
            for (Map<String, Object> item0 : (List<Map<String, Object>>) ListInfoDiscJour) {

                statusDisc.add(item0.get("status").toString());
                date.add(item0.get("date").toString());
            }


        }
        catch (ClassCastException e) {
            e.printStackTrace();
        }
        catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        //Ajouyer les informations aux array

        sanctionArray =sanctions.toArray(new String[sanctions.size()]);
        nombreArray =nombre.toArray(new String[nombre.size()]);

        nomMatiereArray = nomMatiere.toArray(new String[nomMatiere.size()]);
        dateHeureArray =dateHeure.toArray(new String[dateHeure.size()]);
        statusArray =status.toArray(new String[status.size()]);

        statusDiscArray =statusDisc.toArray(new String[statusDisc.size()]);
        dateArray =date.toArray(new String[date.size()]);

        itemSanctionsEleve =new ArrayList<>();
        itemDesciplineEleve=new ArrayList<>();
        itemDiscJourEleves=new ArrayList<>();

            for (int j = 0; j < nomMatiereArray.length; j++) {
                itemDesciplineEleve.add(new ItemDesciplineEleve(
                        nomMatiereArray[j].toString(),
                        dateHeureArray[j].toString(),
                        statusArray[j].toString())); }

        for(int i=0;i<sanctionArray.length;i++) {
            itemSanctionsEleve.add(new ItemSanctionsEleve(
                    sanctionArray[i].toString(),
                    nombreArray[i].toString()));}

        for(int i=0;i<statusDiscArray.length;i++) {
            itemDiscJourEleves.add(new ItemDiscJourEleve(
                    statusDiscArray[i].toString(),
                    dateArray[i].toString()));}

        mAdapter = new AdapterSanctionsEleve(itemSanctionsEleve, InformationsEleve.this);
        rvSanctionsEleve.setAdapter(mAdapter);
        rvSanctionsEleve.getAdapter().notifyDataSetChanged();
        rvSanctionsEleve.scheduleLayoutAnimation();

        DescAdapter = new AdapterDesciplineEleve(itemDesciplineEleve, InformationsEleve.this);
        rvDesciplineEleve.setAdapter( DescAdapter);
        rvDesciplineEleve.getAdapter().notifyDataSetChanged();
        rvDesciplineEleve.scheduleLayoutAnimation();

        discJourAdapter = new AdapterDiscJourEleve(itemDiscJourEleves, InformationsEleve.this);
        rvAbscenceJournaliaireEleve.setAdapter( discJourAdapter);
        rvAbscenceJournaliaireEleve.getAdapter().notifyDataSetChanged();
        rvAbscenceJournaliaireEleve.scheduleLayoutAnimation();

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
            SessionManagement sessionManagement = new SessionManagement(InformationsEleve.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}


