package com.gestion.ecole.ui.enfant;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.odoo.DeleteRegIdOdoo;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetConditionData;
import com.gestion.ecole.odoo.GetConnectionData;
import com.google.firebase.iid.FirebaseInstanceId;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class enfant extends AppCompatActivity {

    CardView cvImage;

    RecyclerView rvEnfantConsulter;
    AdapterEnfant mAdapter;


    ArrayList<ItemEnfant> itemEnfant;


    ArrayList<String> nom=new ArrayList<>();
    ArrayList<String> id=new ArrayList<>();
    ArrayList<String> nomParent=new ArrayList<>();
    ArrayList<String> nomClasse=new ArrayList<>();


    String[] idArray,nomArray,nomParentArray,nomClasseArray;
    String NameParent,res_users,db,url,mdp,intentId, parentID,id_reg;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enfant);


        getSupportActionBar().setDisplayHomeAsUpEnabled(true);


        rvEnfantConsulter=findViewById(R.id.rvEnfantConsulter);
        rvEnfantConsulter.setHasFixedSize(true);





        RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(enfant.this);
        rvEnfantConsulter.setLayoutManager(layoutManager);

        SessionManagement sessionManagement = new SessionManagement(enfant.this);
       parentID = sessionManagement.getId();
        db=sessionManagement.getSESSION_DB();
        url=sessionManagement.getSESSION_URL();
       mdp=sessionManagement.getMdp();
         NameParent = sessionManagement.getNameParent();
         res_users=sessionManagement.getSESSION_RES_USERS();


        AsyncTask<URL, String, List> InfoEleve = new GetConditionData(db,url,mdp,res_users,"student.student", new String[]{"id", "last", "name", "parent_id",
                "standard_id", "parent_id"}, "parent_id.id", parentID).execute();
        try {

                List ListinfoEleve = InfoEleve.get();
                System.out.println("enfant 2 :" + ListinfoEleve);

                //Information eleve
                for (Map<String, Object> item : (List<Map<String, Object>>) ListinfoEleve) {
                    nom.add(item.get("name").toString() + " " + item.get("last").toString());
                    nomParent.add(NameParent);

                    //Nom du claase
                    Object[] standard_id = (Object[]) item.get("standard_id");
                    nomClasse.add(standard_id[1].toString());

                    id.add((item.get("id").toString()));
                }

        }
        catch (ClassCastException e) {
            e.printStackTrace();
        }
        catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        //Ajouyer les informations aux array

        nomArray = nom.toArray(new String[nom.size()]);
        nomParentArray =nomParent.toArray(new String[nomParent.size()]);
        nomClasseArray =nomClasse.toArray(new String[nomClasse.size()]);
        idArray = id.toArray(new String[id.size()]);



        itemEnfant=new ArrayList<>();

        for(int i=0;i<nomArray.length;i++) {


            itemEnfant.add(new ItemEnfant(
                    nomArray[i].toString(),
                    nomParentArray[i].toString(),
                    nomClasseArray[i].toString(),
                    idArray[i].toString()));}




        mAdapter = new AdapterEnfant(itemEnfant, enfant.this);
        rvEnfantConsulter.setAdapter(mAdapter);
        rvEnfantConsulter.getAdapter().notifyDataSetChanged();
        rvEnfantConsulter.scheduleLayoutAnimation();



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
            String registration_id = FirebaseInstanceId.getInstance().getToken();
            AsyncTask<URL, String, List> regMobile  = new Get2ConditionData(db,url,mdp,res_users,"parent.registration", new String[]{"id","reg_id", "parent_id"},
                    "parent_id.id", parentID,"reg_id",registration_id).execute();

            try {

                List regMobileList=regMobile.get();
                for (Map<String, Object> item5 : (List<Map<String, Object>>) regMobileList) {
                    id_reg=item5.get("id").toString();
                    System.out.println("aaa : " + id_reg);


                }
                AsyncTask<URL, String, Boolean> delete  = new DeleteRegIdOdoo(db,url,mdp,res_users,"parent.registration", id_reg).execute();
                System.out.println("delete"+delete.get());
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            SessionManagement sessionManagement = new SessionManagement(enfant
                    .this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}