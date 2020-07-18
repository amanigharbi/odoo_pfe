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
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetConnectionData;

import java.net.URL;
import java.util.List;
import java.util.Map;

import static java.lang.String.valueOf;


public class LoginActivity extends AppCompatActivity {

    Button btLogin;
    EditText email, mdp;
    String id,name_parent;

    @Override
    protected void onStart() {
        super.onStart();

        checkSession();
    }

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
                        String db = "pfe",
                        username = email.getText().toString(),
                        pass = mdp.getText().toString(),
                        url = "http://192.168.1.14:8069";

                AsyncTask<URL, String, String> verif = new ConnectionOdoo(db, username, pass, url, getApplicationContext()).execute();
                AsyncTask<URL, String, List> InfoParent = new GetConnectionData(db,url,pass,"school.parent",
                        new String[]{"name","id","email","student_id"},"email",username).execute();

                AsyncTask<URL, String, List> resUsers = new GetConnectionData(db,url,pass,"res.users",
                        new String[]{"id","login","password"},"login",username).execute();

                try {
                    String test = verif.get();
                    if (test.equals("Connected")) {
                        List listInfoParent = InfoParent.get();
                        List listuser=resUsers.get();
                        for (Map<String, Object> item2 : (List<Map<String, Object>>) listInfoParent) {

                            id=item2.get("id").toString();
                            name_parent=item2.get("name").toString();

                            for (Map<String, Object> item : (List<Map<String, Object>>) listuser) {
                                String idREsUsers=item.get("id").toString();


                                User user = new User(username, pass,idREsUsers,id,name_parent,db,url);

                                SessionManagement sessionManagement = new SessionManagement(LoginActivity.this);
                                sessionManagement.saveSession(user);

                                Intent intent = new Intent(LoginActivity.this, AccueilActivity.class);
                                startActivity(intent);
                            }}  } else {
                        Toast.makeText(getApplicationContext(), "Vérifiez vos informations SVP!!", Toast.LENGTH_LONG).show();
                    }

                }
                catch (Exception e) {
                    e.printStackTrace();
                }


            }
        });

    }



    private void checkSession() {

        SessionManagement sessionManagement = new SessionManagement(LoginActivity.this);
        String  iD = sessionManagement.getId();
        String  name = sessionManagement.getNameParent();

        if( (iD!="") || (name!="")){

            Intent intent = new Intent(LoginActivity.this, AccueilActivity.class);
            startActivity(intent);
        }

    }




}
