package com.gestion.ecole.login;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.gestion.ecole.AccueilActivity;
import com.gestion.ecole.R;
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
                        url = "http://192.168.1.9:8069";
                AsyncTask<URL, String, String> verif = new ConnectionOdoo(db, username, pass, url, getApplicationContext()).execute();
                try {
                    String test = verif.get();
                    if (test.equals("Connected")) {
                        User user = new User(username,pass);
                        SessionManagement sessionManagement = new SessionManagement(LoginActivity.this);
                        sessionManagement.saveSession(user);
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

    @Override
    protected void onStart() {
        super.onStart();

        checkSession();
    }

    private void checkSession() {
        //check if user is logged in
        //if user is logged in --> move to mainActivity

        SessionManagement sessionManagement = new SessionManagement(LoginActivity.this);
        String  userID = sessionManagement.getSession();

        if(userID != "-1"){
            //user id logged in and so move to mainActivity
            Intent intent = new Intent(LoginActivity.this, AccueilActivity.class);
            startActivity(intent);
        }
        else{
            //do nothing
        }
    }
}
