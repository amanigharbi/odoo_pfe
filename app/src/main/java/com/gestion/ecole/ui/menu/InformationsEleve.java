package com.gestion.ecole.ui.menu;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.os.Bundle;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.R;

public class InformationsEleve extends AppCompatActivity {
    ImageView btFavorite,btAccount;
    ImageButton btHome;
    CardView cvImage,cvInfo;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_informations_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        cvImage= findViewById(R.id.cvImage);
        cvInfo = findViewById(R.id.cvInfo);


        cvImage.scheduleLayoutAnimation();
        cvInfo.scheduleLayoutAnimation();

    }
    }

