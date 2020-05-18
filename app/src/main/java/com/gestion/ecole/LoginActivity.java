package com.gestion.ecole;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.gestion.ecole.odoo.ConnectionOdoo;

import java.net.URL;



public class LoginActivity extends AppCompatActivity {

    Button btLogin;
    EditText email, mdp;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);



        email = findViewById(R.id.email);
        mdp = findViewById(R.id.mdp);
        btLogin = findViewById(R.id.btLogin);


        btLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String db = "school",
                        username = email.getText().toString(),
                        pass = mdp.getText().toString(),
                        url = "http://192.168.1.6:8069";
                AsyncTask<URL, String, String> verif = new ConnectionOdoo(db, username, pass, url, getApplicationContext()).execute();
                try {
                    String test = verif.get();
                    if (test.equals("Connected")) {
                        Intent intent = new Intent(LoginActivity.this, AccueilActivity.class);
                        startActivity(intent);
                    } else {
                        Toast.makeText(getApplicationContext(), "not connected", Toast.LENGTH_LONG).show();
                    }

                }
                 catch (Exception e) {
                    e.printStackTrace();
                }


            }
        });

    }
}
