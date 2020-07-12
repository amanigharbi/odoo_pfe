package com.gestion.ecole.ui.menu.EmploisEleve;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;

import com.gestion.ecole.AccueilActivity;
import com.gestion.ecole.R;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.odoo.DeleteRegIdOdoo;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.google.firebase.iid.FirebaseInstanceId;


import android.widget.ListView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;


import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class EmploisEleve extends AppCompatActivity {
    private ListView lvday;

    public static SharedPreferences sharedPreferences;
    public static String SEL_DAY;
    String res_users,db,url,mdp,intentId, parentID,id_reg;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emploie_day);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        SessionManagement sessionManagement = new SessionManagement(EmploisEleve.this);
        res_users=sessionManagement.getSESSION_RES_USERS();
        db=sessionManagement.getSESSION_DB();
        url=sessionManagement.getSESSION_URL();
        mdp=sessionManagement.getMdp();
        lvday = (ListView) findViewById(R.id.rvDay);
        sharedPreferences = getSharedPreferences("MY_DAY", MODE_PRIVATE);

        //Sauvegarder je jour pour qu'on puise l'utiliser dans l'activité suivante
        String[] week = getResources().getStringArray(R.array.Week);

        AdapterDay adapter = new AdapterDay(this, R.layout.view_emploie_day, week);

        lvday.setAdapter(adapter);

        lvday.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                switch(position){
                    case 0: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);
                        sharedPreferences.edit().putString(SEL_DAY, "Monday").apply();
                        break;
                    }
                    case 1: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);

                        sharedPreferences.edit().putString(SEL_DAY, "Tuesday").apply();
                        break;
                    }
                    case 2: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);

                        sharedPreferences.edit().putString(SEL_DAY, "Wednesday").apply();
                        break;
                    }
                    case 3: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);

                        sharedPreferences.edit().putString(SEL_DAY, "Thursday").apply();
                        break;
                    }
                    case 4: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);

                        sharedPreferences.edit().putString(SEL_DAY, "Friday").apply();
                        break;
                    }
                    case 5: {
                        Intent i =new Intent(EmploisEleve.this, Emplois_details.class);
                        Intent intent=getIntent();
                        String intentId=intent.getStringExtra("id");
                        i.putExtra("idEnfant",intentId);
                        startActivity(i);

                        sharedPreferences.edit().putString(SEL_DAY, "Saturday").apply();
                        break;
                    }
                    default:break;
                }
            }
        });


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
                    System.out.println("aaa : " + id_reg);


                }
                AsyncTask<URL, String, Boolean> delete  = new DeleteRegIdOdoo(db,url,mdp,res_users,"parent.registration", id_reg).execute();
                System.out.println("delete"+delete.get());
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            SessionManagement sessionManagement = new SessionManagement(EmploisEleve.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}

