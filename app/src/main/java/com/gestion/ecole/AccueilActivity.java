package com.gestion.ecole;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.ui.home.HomeFragment;
import com.gestion.ecole.ui.menu.MenuFragment;
import com.gestion.ecole.ui.notif.NotifActivity;
import com.google.firebase.iid.FirebaseInstanceId;

public class AccueilActivity extends AppCompatActivity implements View.OnClickListener {

    ImageView btMenu,btNotification;
    ImageButton btAccueil;

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accueil);

        System.out.println("mainactivitys : " + FirebaseInstanceId.getInstance().getToken());


        //notification
      /* AlarmManager alarmManager = (AlarmManager) getSystemService(Context.ALARM_SERVICE);

        Intent notificationIntent = new Intent(this, AlarmReceiver.class);

        PendingIntent broadcast = PendingIntent.getBroadcast(this, 100, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT);

        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.SECOND, 2);
        alarmManager.setExact(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), broadcast);*/










        loadFragment(new HomeFragment());

        btAccueil      = findViewById(R.id.btAccueil);
        btMenu  = findViewById(R.id.btMenu);
        btNotification   = findViewById(R.id.btNotification);

        btAccueil.setOnClickListener(this);
        btMenu.setOnClickListener(this);
        btNotification.setOnClickListener(this);
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
            case R.id.btAccueil :
                loadFragment(new HomeFragment());
                break;
            case R.id.btMenu:
                loadFragment(new MenuFragment());
                break;
            case R.id.btNotification :
               //loadFragment(new NotifFragment());
                Intent i = new Intent(this, NotifActivity.class);
                startActivity(i);
                break;
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
            // Clear the User session data
            // and redirect user to LoginActivity
            SessionManagement sessionManagement = new SessionManagement(AccueilActivity.this);
            sessionManagement.removeSession();

            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }
        return true;
    }
}
