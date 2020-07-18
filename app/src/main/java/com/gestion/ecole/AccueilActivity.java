package com.gestion.ecole;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.odoo.CreateRegId;
import com.gestion.ecole.odoo.DeleteRegIdOdoo;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.ui.enfant.enfant;
import com.gestion.ecole.ui.home.HomeFragment;
import com.gestion.ecole.ui.menu.MenuFragment;
import com.gestion.ecole.ui.notif.NotifActivity;
import com.google.firebase.iid.FirebaseInstanceId;

import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class AccueilActivity extends AppCompatActivity implements View.OnClickListener {

    ImageView btMenu,btNotification;
    ImageButton btAccueil;
    AsyncTask<URL, String,Boolean> createRegId;
    String parentID, res_users,db,url,mdp,reg;
    String registration_id,id_reg;
    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accueil);

        //Session parent
        SessionManagement sessionManagement = new SessionManagement(AccueilActivity.this);
        parentID = sessionManagement.getId();
        res_users=sessionManagement.getSESSION_RES_USERS();
        db=sessionManagement.getSESSION_DB();
        url=sessionManagement.getSESSION_URL();
        mdp=sessionManagement.getMdp();

        //registration_id : clé du mobile
        registration_id =FirebaseInstanceId.getInstance().getToken();

        AsyncTask<URL, String, List> regMobile  = new GetConditionData(db,url,mdp,res_users,"parent.registration", new String[]{"reg_id", "parent_id"},
                "parent_id.id", parentID).execute();

        try {

            List regMobileList=regMobile.get();
            for (Map<String, Object> item5 : (List<Map<String, Object>>) regMobileList) {
                reg=item5.get("reg_id").toString();
            }
            //s'il n'y a pas de registration pour le parent, il va le crée
            if(!(registration_id.equals(reg))) {
                createRegId = new CreateRegId (db,url,mdp,res_users,"parent.registration","reg_id",registration_id,"parent_id",parentID).execute();
                System.out.println("createRegId"+createRegId.get());

            }
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


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
            AsyncTask<URL, String, List> regMobile  = new Get2ConditionData(db,url,mdp,res_users,"parent.registration", new String[]{"id","reg_id", "parent_id"},
                    "parent_id.id", parentID,"reg_id",registration_id).execute();

            try {

                List regMobileList=regMobile.get();
                for (Map<String, Object> item5 : (List<Map<String, Object>>) regMobileList) {
                    id_reg=item5.get("id").toString();
                }
                //Supprimer le registration id du parent
                AsyncTask<URL, String, Boolean> delete  = new DeleteRegIdOdoo(db,url,mdp,res_users,"parent.registration", id_reg).execute();

            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // Supprimer la session du parent
            // Redirect parent dans la page du login
            SessionManagement sessionManagement = new SessionManagement(AccueilActivity.this);
            sessionManagement.removeSession();

            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }
        return true;
    }
}
