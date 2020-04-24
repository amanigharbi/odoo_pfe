package com.gestion.ecole.ui.menu.EmploisEleve;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageButton;
import com.gestion.ecole.R;


import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;


import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetDataOdoo;

import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class EmploisEleve extends AppCompatActivity {
    TextView jourArr,matiereArr,debutArr,finArr;
    TableLayout table;
    TableRow tr;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emplois_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        table=findViewById(R.id.table);
        for(int i=0;i<table.getWidth();i++){
            table.setColumnShrinkable(i,true);
        }

        try{
            //Extraire id du classe du table eleve.eleve
            AsyncTask<URL,String, List> standard_eleve = new GetDataOdoo("eleve.eleve",
                    new String[]{"standard_id"}).execute();
            List stan = standard_eleve.get();


            for(Map<String,Object> item0 : (List<Map<String,Object>>) stan) {
                Object[] standard = (Object[]) item0.get("standard_id");

                //Asocier id du classe du table  eleve.eleve avec table emploie.emploie
                AsyncTask<URL, String, List> emploie = new GetConditionData("emploie.emploie", new String[]{"id", "standard_id"},
                        "standard_id.id",standard[0].toString() ).execute();

                List emploie_id = emploie.get();

                //Associer id d'emploie du table emploie.emploie avec table emploie.emploie.line
                for (Map<String, Object> item1 : (List<Map<String, Object>>) emploie_id) {
                    AsyncTask<URL, String, List> info = new GetConditionData("emploie.emploie.line", new String[]{"start_time", "subject_id", "end_time", "week_day", "table_id"},
                            "table_id.id", item1.get("id").toString()).execute();

                    List resultat = info.get();


                    //Ajouter les informations au tableRow et tableLayout
                    for (Map<String, Object> item : (List<Map<String, Object>>) resultat) {

                        tr = new TableRow(this);
                        tr.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT));
                        jourArr = new TextView(this);
                        matiereArr = new TextView(this);
                        debutArr = new TextView(this);
                        finArr = new TextView(this);


                        jourArr.setText(item.get("week_day").toString());
                        jourArr.setGravity(Gravity.CENTER);
                        jourArr.setTextSize(14);
                        jourArr.setPadding(0,5,0,0);
                        jourArr.setWidth(150);
                        jourArr.setBackgroundColor(Color.WHITE);


                        Object[] mat = (Object[]) item.get(("subject_id"));
                            matiereArr.setText(mat[1].toString());
                            matiereArr.setGravity(Gravity.CENTER);
                            matiereArr.setTextSize(14);
                            matiereArr.setWidth(220);


                        debutArr.setText(item.get("start_time").toString());
                        debutArr.setGravity(Gravity.CENTER);
                        debutArr.setTextSize(14);
                        debutArr.setWidth(180);
                        debutArr.setPadding(0,5,0,0);
                        debutArr.setBackgroundColor(Color.WHITE);

                        finArr.setText(item.get("end_time").toString());
                        finArr.setGravity(Gravity.CENTER);
                        finArr.setTextSize(14);
                        finArr.setWidth(150);
                        finArr.setRight(1);
                        finArr.setBottom(1);


                        tr.addView(jourArr);
                        tr.addView(matiereArr);
                        tr.addView(debutArr);
                        tr.addView(finArr);

                        table.addView(tr);
                    }

                }}

        }catch (ExecutionException e){
            e.printStackTrace();
        } catch (InterruptedException e){
            e.printStackTrace();
        }


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
         }else{
        this.finish();
    }
        return true;
    }

    }

