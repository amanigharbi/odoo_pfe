package com.gestion.ecole.ui.menu;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.widget.ImageButton;

import com.gestion.ecole.R;

import java.util.ArrayList;

public class ContactEnseignant extends AppCompatActivity {

    ImageButton btHome;

    RecyclerView rvContact;
    AdapterContactEns mAdapter;
    String ContactEnsg[]={"Enseignant","Enseignant","Enseignant"};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact_enseignant);

        getSupportActionBar().setDisplayHomeAsUpEnabled(true);





        rvContact = findViewById(R.id.rvContact);
        rvContact.setHasFixedSize(true);

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(ContactEnseignant.this);
        rvContact.setLayoutManager(layoutManager);

        ArrayList<String> listContact = new ArrayList<>();
        listContact.add(ContactEnsg[0]);
        listContact.add(ContactEnsg[1]);
        listContact.add(ContactEnsg[2]);

        mAdapter = new AdapterContactEns(listContact,ContactEnseignant.this);
        rvContact.setAdapter(mAdapter);

        rvContact.getAdapter().notifyDataSetChanged();
        rvContact.scheduleLayoutAnimation();


    }




}
