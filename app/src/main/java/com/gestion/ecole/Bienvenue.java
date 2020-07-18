package com.gestion.ecole;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;

public class Bienvenue extends AppCompatActivity {
    ImageView logo;
    TextView tvAppName;
    Animation leftoright,righttoleft;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bienvenue);

        logo        = findViewById(R.id.logo);
        tvAppName   = findViewById(R.id.tvAppName);

        leftoright  = AnimationUtils.loadAnimation(this,R.anim.lefttoright);
        righttoleft = AnimationUtils.loadAnimation(this,R.anim.righttoleft);

        logo.setAnimation(righttoleft);
        tvAppName.setAnimation(leftoright);

        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent a = new Intent(Bienvenue.this, Introduction.class);
                startActivity(a);
                finish();
            }
        },1500);
    }

    }
