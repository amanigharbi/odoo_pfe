package com.gestion.ecole;

import androidx.appcompat.app.AppCompatActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.gestion.ecole.ConnectionOdoo;

import java.net.URL;


public class LoginActivity extends AppCompatActivity {
 Button btLogin;

 private int proPer=0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
final EditText email = findViewById(R.id.etUsername);
final EditText pwd = findViewById(R.id.etPassword);
        btLogin=findViewById(R.id.btLogin);

        btLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String db ="ecole_bd",
                        username=email.getText().toString(),
                        pass=pwd.getText().toString(),
                        url="http://localhost:8068";
                AsyncTask<URL,String,String> verif =new ConnectionOdoo(db,username,pass, url,getApplicationContext()).execute();
                try {
                    String test=verif.get();
                    if (test.equals("Connected")){
                        Intent intent = new Intent(LoginActivity.this,AccueilActivity.class);
                        startActivity(intent);
                    }
                    else {
                        Toast.makeText(getApplicationContext(),"not connected",Toast.LENGTH_LONG).show();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }


            }
        });
    }
}
