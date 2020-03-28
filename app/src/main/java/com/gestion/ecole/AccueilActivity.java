package com.gestion.ecole;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.ui.home.HomeFragment;
import com.gestion.ecole.ui.menu.MenuFragment;
import com.gestion.ecole.ui.notif.AlarmReceiver;
import com.gestion.ecole.ui.notif.NotifFragment;

import java.util.Calendar;

public class AccueilActivity extends AppCompatActivity implements View.OnClickListener {

    ImageView btFavorite,btAccount;
    ImageButton btHome;

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accueil);



        //notification
        AlarmManager alarmManager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);

        Intent notificationIntent = new Intent(this, AlarmReceiver.class);
        PendingIntent broadcast = PendingIntent.getBroadcast(this, 100, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT);

        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.SECOND, 2);
        alarmManager.setExact(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), broadcast);


        loadFragment(new HomeFragment());

        btHome      = findViewById(R.id.btHome);
        btFavorite  = findViewById(R.id.btFavorite);
        btAccount   = findViewById(R.id.btAccount);

        btHome.setOnClickListener(this);
        btFavorite.setOnClickListener(this);
        btAccount.setOnClickListener(this);
    }

    private boolean loadFragment(Fragment fragment) {
        if (fragment!=null){
            FragmentManager fragmentManager         = getSupportFragmentManager();
            FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
            fragmentTransaction.replace(R.id.container,fragment);
            fragmentTransaction.setCustomAnimations(android.R.anim.fade_in,android.R.anim.fade_out);
            fragmentTransaction.commit();
            return true;
        }
        return false;
    }


    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.btHome :
                loadFragment(new HomeFragment());
                break;
            case R.id.btFavorite:
                loadFragment(new MenuFragment());
                break;
            case R.id.btAccount :
                loadFragment(new NotifFragment());
                break;
        }
    }
}
