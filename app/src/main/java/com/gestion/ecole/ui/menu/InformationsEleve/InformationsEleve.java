package com.gestion.ecole.ui.menu.InformationsEleve;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.R;
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

    RecyclerView rvInformationsEleve;
    AdapterInfoEleve mAdapter;

    ArrayList<ItemInfoEleve> itemInfoEleve;

    ArrayList<String> nom=new ArrayList<>();
    ArrayList<String> prenom=new ArrayList<>();
    ArrayList<String> nomParent=new ArrayList<>();
    ArrayList<String> nomClasse=new ArrayList<>();

    String[] nomArray,prenomArray,nomParentArray,nomClasseArray;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_informations_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        cvImage= findViewById(R.id.cvImage);
        cvInfo = findViewById(R.id.cvInfo);
        rvInformationsEleve=findViewById(R.id.rvInformationsEleve);
        rvInformationsEleve.setHasFixedSize(true);


        cvImage.scheduleLayoutAnimation();
      //  cvInfo.scheduleLayoutAnimation();

        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InformationsEleve.this);
        rvInformationsEleve.setLayoutManager(layoutManager);



      //consommation information élève
        AsyncTask<URL, String, List> InfoEleve=new GetDataOdoo("eleve.eleve", new String[]{"eleve_name","parent_id",
                "standard_id"},null);
        InfoEleve.execute();

        try {
            List Listinfo=InfoEleve.get();

            for(Map<String,Object> item: (List<Map<String,Object>>) Listinfo){
                nom.add(item.get("eleve_name").toString());
              //  prenom.add(item.get("name").toString());
                nomParent.add(item.get("parent_id").toString());
                nomClasse.add(item.get("standard_id").toString());
            }
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        nomArray = nom.toArray(new String[nom.size()]);
      //  prenomArray = prenom.toArray(new String[prenom.size()]);
        nomClasseArray =nomClasse.toArray(new String[nomClasse.size()]);

        itemInfoEleve=new ArrayList<>();
        for(int i=0;i<nomArray.length;i++)
        {
            itemInfoEleve.add(new ItemInfoEleve(nomArray[i].toString(),
                  //  prenomArray[i].toString(),
                    nomParentArray[i].toString(),
                    nomClasseArray[i].toString() ));
        }

        mAdapter = new AdapterInfoEleve(itemInfoEleve,InformationsEleve.this);
        rvInformationsEleve.setAdapter(mAdapter);

        rvInformationsEleve.getAdapter().notifyDataSetChanged();
        rvInformationsEleve.scheduleLayoutAnimation();

    }



}


