package com.gestion.ecole.ui.menu.ContactEnseignant;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;

import com.gestion.ecole.R;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetDataOdoo;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class ContactEnseignant extends AppCompatActivity {

    ImageButton btHome;

    RecyclerView rvEnseignant;
    AdapterContactEns mAdapter;

    ArrayList<ItemEnseignant> itemEnseignant;

    ArrayList<String> nomPrenom=new ArrayList<>();
    ArrayList<String> email=new ArrayList<>();
    ArrayList<String> numero=new ArrayList<>();
    ArrayList<String> matiere=new ArrayList<>();

    String[] nomPrenomArray,emailArray,numeroArray,matiereArray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact_enseignant);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);


        rvEnseignant = findViewById(R.id.rvEnseignant);
        rvEnseignant.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(ContactEnseignant.this);
        rvEnseignant.setLayoutManager(layoutManager);


        try {

        //Extraire id d'emploie du table emploie.emploie
        AsyncTask<URL,String, List> standard_eleve = new GetDataOdoo("emploie.emploie",
                new String[]{"id"}).execute();
        List stan = standard_eleve.get();

            for(Map<String,Object> item0 : (List<Map<String,Object>>) stan) {
               //Associer id d'emploie du table emploie.emploie avec celle du table emploie.emploie.line
                AsyncTask<URL, String, List> emploie2 = new GetConditionData("emploie.emploie.line",
                        new String[]{"enseignant_id", "table_id","subject_id"}, "table_id.id", item0.get("id").toString()).execute();
                List Listemploie2 = emploie2.get();


                for(Map<String,Object> item1 : (List<Map<String,Object>>) Listemploie2) {
                    Object[] emploie = (Object[]) item1.get("enseignant_id");

                    //Associer id d'enseignant du table emploie.emploie.line avec celle du table ecole.enseignant
                    AsyncTask<URL, String, List> InfoEnseignant = new GetConditionData("ecole.enseignant", new String[]{"name", "work_email",
                            "phone_numbers", "id","subject_id"}, "id", emploie[0].toString()).execute();
                    List Listinfo = InfoEnseignant.get();


                    for(Map<String,Object> item: (List<Map<String,Object>>) Listinfo){
                        //Utiliser subject_id du table emploie.emploie.line pour le nom mattière
                    Object[] matt = (Object[])item1.get("subject_id");


                  //Ajouter les attributs dans array
                nomPrenom.add(item.get("name").toString());
                email.add(item.get("work_email").toString());
                numero.add(item.get("phone_numbers").toString());
                matiere.add(matt[1].toString());
            }}}
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        nomPrenomArray = nomPrenom.toArray(new String[nomPrenom.size()]);
        emailArray = email.toArray(new String[email.size()]);
        numeroArray =numero.toArray(new String[numero.size()]);
        matiereArray =matiere.toArray(new String[matiere.size()]);

        itemEnseignant=new ArrayList<>();
        for(int i=0;i<nomPrenomArray.length;i++)
        {
            itemEnseignant.add(new ItemEnseignant(nomPrenomArray[i].toString(),
                    emailArray[i].toString(),
                    numeroArray[i].toString(),
                    matiereArray[i].toString()));
        }

        mAdapter = new AdapterContactEns(itemEnseignant,ContactEnseignant.this);
        rvEnseignant.setAdapter(mAdapter);

        rvEnseignant.getAdapter().notifyDataSetChanged();
        rvEnseignant.scheduleLayoutAnimation();

    }

//POur tolbar , menu,back button
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
        }else{
            this.finish();
        }
        return true;
    }

}
