package com.gestion.ecole.ui.menu;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.ImageButton;

import com.gestion.ecole.R;

public class EmploisEleve extends AppCompatActivity {

    ImageButton btHome;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emplois_eleve);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

    }
}
