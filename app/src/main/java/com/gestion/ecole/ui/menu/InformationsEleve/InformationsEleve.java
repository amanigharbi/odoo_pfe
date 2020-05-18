package com.gestion.ecole.ui.menu.InformationsEleve;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.R;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetDataOdoo;


import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class InformationsEleve extends AppCompatActivity {
    ImageView btFavorite,btAccount;
    ImageButton btHome;
    CardView cvImage,cvInfo;

    RecyclerView rvInformationsEleve,rvDesciplineEleve;
    AdapterInfoEleve mAdapter;
    AdapterDesciplineEleve DescAdapter;

    ArrayList<ItemInfoEleve> itemInfoEleve;
    ArrayList<ItemDesciplineEleve> itemDesciplineEleve;

    ArrayList<String> nom=new ArrayList<>();
    ArrayList<String> prenom=new ArrayList<>();
    ArrayList<String> nomParent=new ArrayList<>();
    ArrayList<String> nomClasse=new ArrayList<>();
    ArrayList<String> nomMatiere=new ArrayList<>();
    ArrayList<String> dateHeure=new ArrayList<>();
    ArrayList<String> status=new ArrayList<>();

    String[] nomArray,prenomArray,nomParentArray,nomClasseArray,nomMatiereArray,dateHeureArray,statusArray;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_informations_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        cvImage= findViewById(R.id.cvImage);

        rvInformationsEleve=findViewById(R.id.rvInformationsEleve);
        rvInformationsEleve.setHasFixedSize(true);

        rvDesciplineEleve=findViewById(R.id.rvDesciplineEleve);
        rvDesciplineEleve.setHasFixedSize(true);


        cvImage.scheduleLayoutAnimation();
      //  cvInfo.scheduleLayoutAnimation();

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InformationsEleve.this);
        RecyclerView.LayoutManager layoutManager2 = new LinearLayoutManager(InformationsEleve.this);
        rvInformationsEleve.setLayoutManager(layoutManager);
       rvDesciplineEleve.setLayoutManager(layoutManager2);


        AsyncTask<URL, String, List> InfoEleve = new GetDataOdoo("student.student", new String[]{"id","last", "name", "parent_id",
                "standard_id"}).execute();


        AsyncTask<URL, String, List> InfoParent = new GetDataOdoo("school.parent", new String[]{"name"}).execute();



        try {

               List ListinfoEleve = InfoEleve.get();
               List listInfoParent = InfoParent.get();

               //Information eleve
               for (Map<String, Object> item : (List<Map<String, Object>>) ListinfoEleve) {
                   nom.add(item.get("name").toString()+" "+item.get("last").toString());
                   //prenom.add(item.get("name").toString());

                   //Information Parent
                   for (Map<String, Object> item2 : (List<Map<String, Object>>) listInfoParent) {
                       nomParent.add((item2.get("name").toString())); }

                   //Nom du claase
                   Object[] standard_id=(Object[]) item.get("standard_id");
                   nomClasse.add(standard_id[1].toString());

                   //Informations Descipline
                   AsyncTask<URL, String, List> infoDescipline = new GetConditionData("student.desciplines", new String[]{"student_id","subject_id", "device_datetime", "status"},
                           "student_id.id",item.get("id").toString()).execute();

                   List ListInfoDescipline = infoDescipline.get();

                   for (Map<String, Object> item5 : (List<Map<String, Object>>) ListInfoDescipline) {

                       Object[] mat = (Object[]) item5.get("subject_id");
                       nomMatiere.add(mat[1].toString());

                       dateHeure.add(item5.get("device_datetime").toString());
                       status.add(item5.get("status").toString());
                   }
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
        nomArray = nom.toArray(new String[nom.size()]);
      //  prenomArray = prenom.toArray(new String[prenom.size()]);
        nomParentArray =nomParent.toArray(new String[nomParent.size()]);
        nomClasseArray =nomClasse.toArray(new String[nomClasse.size()]);

        nomMatiereArray = nomMatiere.toArray(new String[nomMatiere.size()]);
        dateHeureArray =dateHeure.toArray(new String[dateHeure.size()]);
        statusArray =status.toArray(new String[status.size()]);


        itemInfoEleve=new ArrayList<>();
        itemDesciplineEleve=new ArrayList<>();
        for(int i=0;i<nomArray.length;i++) {


                itemInfoEleve.add(new ItemInfoEleve(nomArray[i].toString(),
                      //  prenomArray[i].toString(),
                        nomParentArray[i].toString(),
                        nomClasseArray[i].toString()));}


            for (int j = 0; j < nomMatiereArray.length; j++) {
                itemDesciplineEleve.add(new ItemDesciplineEleve(
                        nomMatiereArray[j].toString(),
                        dateHeureArray[j].toString(),
                        statusArray[j].toString())); }

        mAdapter = new AdapterInfoEleve(itemInfoEleve,InformationsEleve.this);
        rvInformationsEleve.setAdapter(mAdapter);
        rvInformationsEleve.getAdapter().notifyDataSetChanged();
        rvInformationsEleve.scheduleLayoutAnimation();

        DescAdapter = new AdapterDesciplineEleve(itemDesciplineEleve,InformationsEleve.this);
        rvDesciplineEleve.setAdapter( DescAdapter);
        rvDesciplineEleve.getAdapter().notifyDataSetChanged();
        rvDesciplineEleve.scheduleLayoutAnimation();

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
            Intent intent = new Intent(this,com.gestion.ecole.LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}


