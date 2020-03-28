package com.gestion.ecole;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import com.gestion.ecole.ui.notif.NotifFragment;

public class NotifActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.notif_activity);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .replace(R.id.container, NotifFragment.newInstance())
                    .commitNow();
        }
    }
}
