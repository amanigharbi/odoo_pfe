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
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetConnectionData;
import com.gestion.ecole.ui.enfant.enfant;


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
            SessionManagement sessionManagement = new SessionManagement(ContactEnseignant.this);
            String db=sessionManagement.getSESSION_DB();
            String url=sessionManagement.getSESSION_URL();
            String mdp=sessionManagement.getMdp();
            String res_users=sessionManagement.getSESSION_RES_USERS();

            Intent intent=getIntent();
            String intentId=intent.getStringExtra("id");
            //Assicier id élève du table student.student avec school.teacher
            AsyncTask<URL, String, List> InfoEnseignant = new GetConditionData(db,url,mdp,res_users,"school.teacher", new String[]{"name", "work_email",
                    "phone_numbers", "id","subject_id","student_id"},"stud_id.id",intentId).execute();
            List ListinfoEnseig = InfoEnseignant.get();


            for(Map<String,Object> item: (List<Map<String,Object>>) ListinfoEnseig) {
                //Ajouter les attributs dans array
                System.out.println("name"+item.get("name").toString());
                nomPrenom.add(item.get("name").toString());
                email.add(item.get("work_email").toString());
                numero.add(item.get("phone_numbers").toString());


            } }catch (ExecutionException e) {
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
                    numeroArray[i].toString()
            ));
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
            SessionManagement sessionManagement = new SessionManagement(ContactEnseignant.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}
