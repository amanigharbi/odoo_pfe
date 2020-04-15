package com.gestion.ecole.ui.menu.ContactEnseignant;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.ImageButton;

import com.gestion.ecole.R;
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

    String[] nomPrenomArray,emailArray,numeroArray;

    String ContactEnsg[]={"Enseignant","Enseignant","Enseignant"};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact_enseignant);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);


        rvEnseignant = findViewById(R.id.rvEnseignant);
        rvEnseignant.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(ContactEnseignant.this);
        rvEnseignant.setLayoutManager(layoutManager);


       /* ArrayList<ItemEnseignant> listContact = new ArrayList<>();
        listContact.add(ContactEnsg[0]);
        listContact.add(ContactEnsg[1]);
        listContact.add(ContactEnsg[2]);

        mAdapter = new AdapterContactEns(listContact,ContactEnseignant.this);
        rvEnseignant.setAdapter(mAdapter);

        rvEnseignant.getAdapter().notifyDataSetChanged();
        rvEnseignant.scheduleLayoutAnimation();*/


       //Consultation des info enseignants de odoo
        AsyncTask<URL, String, List> InfoEnseignant=new GetDataOdoo("ecole.enseignant", new String[]{"name","work_email",
                "phone_numbers"},null);
        InfoEnseignant.execute();

        try {
            List Listinfo=InfoEnseignant.get();

            for(Map<String,Object> item: (List<Map<String,Object>>) Listinfo){
                nomPrenom.add(item.get("name").toString());
                email.add(item.get("work_email").toString());
                numero.add(item.get("phone_numbers").toString());
            }
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        nomPrenomArray = nomPrenom.toArray(new String[nomPrenom.size()]);
        emailArray = email.toArray(new String[email.size()]);
        numeroArray =numero.toArray(new String[numero.size()]);

        itemEnseignant=new ArrayList<>();
        for(int i=0;i<nomPrenomArray.length;i++)
        {
            itemEnseignant.add(new ItemEnseignant(nomPrenomArray[i].toString(),
                    emailArray[i].toString(),
                    numeroArray[i].toString() ));
        }

        mAdapter = new AdapterContactEns(itemEnseignant,ContactEnseignant.this);
        rvEnseignant.setAdapter(mAdapter);

        rvEnseignant.getAdapter().notifyDataSetChanged();
        rvEnseignant.scheduleLayoutAnimation();

    }




}
