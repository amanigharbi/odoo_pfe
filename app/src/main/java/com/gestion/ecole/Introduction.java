package com.gestion.ecole;

import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.gestion.ecole.login.LoginActivity;
import com.google.android.material.tabs.TabLayout;

import java.util.ArrayList;
import java.util.List;

public class Introduction extends AppCompatActivity {
    ViewPager viewPager;
    TabLayout tabLayout;
    TextView btSkip,btNext;
    Button btGetStarted;
    AdapterIntroViewPager mAdapter;

  /*  String prevStarted = "prevStarted";
    @Override
    protected void onResume() {
        super.onResume();
        SharedPreferences sharedPrefences = getSharedPreferences(getString(R.string.app_name), Context.MODE_PRIVATE);
        if(!sharedPrefences.getBoolean(prevStarted,false)){
            SharedPreferences.Editor editor= sharedPrefences.edit();
            editor.putBoolean(prevStarted,Boolean.TRUE);
            editor.apply();
        }else{
            finish();
        }
    }*/


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_introduction);


         /* SharedPreferences settings=getSharedPreferences("prefs",0);
        boolean firstRun=settings.getBoolean("firstRun",false);
        if(firstRun==false)//if running for first time
        //Splash will load for first time
        {
            SharedPreferences.Editor editor=settings.edit();
            editor.putBoolean("firstRun",true);
            editor.commit();
           // Intent i=new Intent(Introduction.this, LoginActivity.class);
            //startActivity(i);
            //finish();
        }
        else
        {

            Intent a=new Intent(Introduction.this,LoginActivity.class);
            startActivity(a);  // Launch next activity
            finish();
        }*/



        viewPager       = findViewById(R.id.viewpager);
        tabLayout       = findViewById(R.id.tablayout);
        btSkip          = findViewById(R.id.btSkip);
        btNext          = findViewById(R.id.btNext);
        btGetStarted    = findViewById(R.id.btGetStarted);


        btGetStarted.setVisibility(View.GONE);
        final List<ScreenItem> arrayList = new ArrayList<>();
        arrayList.add(new ScreenItem( "Éleve","Vous trouvez ici les informations nécessaires \n de votre enfant!",R.drawable.teacher1));
        arrayList.add(new ScreenItem( "Enseignant","Vous trouvez ici les contacts des enseignants \n de votre enfant!",R.drawable.enseignant));
        arrayList.add(new ScreenItem("École","à tout moment vous pouvez nous contacter!", R.drawable.school));



        mAdapter    = new AdapterIntroViewPager(this,arrayList);
        viewPager.setAdapter(mAdapter);

        tabLayout.setupWithViewPager(viewPager);

        tabLayout.addOnTabSelectedListener(new TabLayout.BaseOnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                if (tab.getPosition()==arrayList.size()-1){
                    loadLastScreen();
                }
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });

        btSkip.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                viewPager.setCurrentItem(arrayList.size());

            }
        });

        btNext.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int position    =0;
                position        = viewPager.getCurrentItem();
                if (position<arrayList.size()) {
                    position++;
                    viewPager.setCurrentItem(position);
                }

                if (position==arrayList.size()-1){
                    loadLastScreen();
                }
            }
        });

        btGetStarted.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(Introduction.this, LoginActivity.class);
                startActivity(i);
                finish();
            }
        });
    }

    private void loadLastScreen() {
        btSkip.setVisibility(View.INVISIBLE);
        btNext.setVisibility(View.INVISIBLE);
        tabLayout.setVisibility(View.INVISIBLE);
        btGetStarted.setVisibility(View.VISIBLE);
    }
}