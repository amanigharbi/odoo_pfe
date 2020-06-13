package com.gestion.ecole.ui.menu.EmploisEleve;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;

import com.gestion.ecole.AccueilActivity;
import com.gestion.ecole.R;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.login.LoginActivity;


import android.widget.ListView;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;


import java.util.ArrayList;

public class EmploisEleve extends AppCompatActivity {
    private ListView lvday;

    public static SharedPreferences sharedPreferences;
    public static String SEL_DAY;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emploie_day);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

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

