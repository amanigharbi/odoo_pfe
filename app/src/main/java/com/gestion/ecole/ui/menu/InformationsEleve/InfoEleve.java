package com.gestion.ecole.ui.menu.InformationsEleve;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.app.Dialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.gestion.ecole.R;
import com.gestion.ecole.login.LoginActivity;
import com.gestion.ecole.login.SessionManagement;
import com.gestion.ecole.odoo.DeleteRegIdOdoo;
import com.gestion.ecole.odoo.Get2ConditionData;
import com.gestion.ecole.odoo.GetConditionData;
import com.google.firebase.iid.FirebaseInstanceId;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class InfoEleve extends AppCompatActivity {
    CardView cardSanction,cardDiscMatiere,cardDiscJour ;
    Dialog myDialog;
    LinearLayout ll;
    String res_users,db,url,mdp,intentId, parentID,id_reg;
    SessionManagement sessionManagement;
    Intent intent;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_info_eleve);
        ll = (LinearLayout) findViewById(R.id.ll);
        cardDiscMatiere = (CardView) findViewById(R.id.cardDiscMatiere);
        cardDiscJour = (CardView) findViewById(R.id.cardDiscJour);
        cardSanction = (CardView) findViewById(R.id.cardSanction);
        myDialog = new Dialog(this);


      sessionManagement = new SessionManagement(InfoEleve.this);
        parentID = sessionManagement.getId();
         res_users=sessionManagement.getSESSION_RES_USERS();
         db=sessionManagement.getSESSION_DB();
       url=sessionManagement.getSESSION_URL();
         mdp=sessionManagement.getMdp();

         intent=getIntent();
        intentId=intent.getStringExtra("id");


        cardDiscMatiere.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                RecyclerView rvDesciplineEleve;
                AdapterDisciplineEleve DescAdapter;
                ArrayList<ItemDesciplineEleve> itemDesciplineEleve;

                ArrayList<String> nomMatiere=new ArrayList<>();
                ArrayList<String> dateHeure=new ArrayList<>();
                ArrayList<String> status=new ArrayList<>();

                TextView txtclose;
                String[] nomMatiereArray,dateHeureArray,statusArray;

                myDialog.setContentView(R.layout.activity_discipline_matiere);
                txtclose =(TextView) myDialog.findViewById(R.id.txtclose);


                rvDesciplineEleve=myDialog.findViewById(R.id.rvDesciplineEleve);
                rvDesciplineEleve.setHasFixedSize(true);
                RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InfoEleve.this);
                rvDesciplineEleve.setLayoutManager(layoutManager);


                try {

                    //Informations Discipline
                    AsyncTask<URL, String, List> infoDescipline = new GetConditionData(db,url,mdp,res_users,"student.disciplines", new String[]{"student_id", "subject_id", "device_datetime", "status"},
                            "student_id.id", intentId).execute();
                    List ListInfoDescipline = infoDescipline.get();


                    for (Map<String, Object> item5 : (List<Map<String, Object>>) ListInfoDescipline) {

                        Object[] mat = (Object[]) item5.get("subject_id");
                        nomMatiere.add(mat[1].toString());

                        dateHeure.add(item5.get("device_datetime").toString());
                        status.add(item5.get("status").toString());
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

                nomMatiereArray = nomMatiere.toArray(new String[nomMatiere.size()]);
                dateHeureArray =dateHeure.toArray(new String[dateHeure.size()]);
                statusArray =status.toArray(new String[status.size()]);

                itemDesciplineEleve=new ArrayList<>();
                for (int j = 0; j < nomMatiereArray.length; j++) {
                    itemDesciplineEleve.add(new ItemDesciplineEleve(
                            nomMatiereArray[j].toString(),
                            dateHeureArray[j].toString(),
                            statusArray[j].toString())); }



                DescAdapter = new AdapterDisciplineEleve(itemDesciplineEleve, InfoEleve.this);
                rvDesciplineEleve.setAdapter( DescAdapter);
                rvDesciplineEleve.getAdapter().notifyDataSetChanged();
                rvDesciplineEleve.scheduleLayoutAnimation();


                txtclose.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        myDialog.dismiss();
                    }
                });
                myDialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
                myDialog.show();
            }
        });



        cardDiscJour.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                RecyclerView rvAbscenceJournaliaireEleve;
                AdapterDiscJourEleve discJourAdapter;
                ArrayList<ItemDiscJourEleve>itemDiscJourEleves;

                ArrayList<String> statusDisc=new ArrayList<>();
                ArrayList<String> date=new ArrayList<>();
                TextView txtclose,tvTitre;
                String[] statusDiscArray,dateArray;
                myDialog.setContentView(R.layout.activity_discipline_jour);
                txtclose =(TextView) myDialog.findViewById(R.id.txtclose);


                rvAbscenceJournaliaireEleve= myDialog.findViewById(R.id.rvAbscenceJournaliaireEleve);
                rvAbscenceJournaliaireEleve.setHasFixedSize(true);

                RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InfoEleve.this);
                rvAbscenceJournaliaireEleve.setLayoutManager(layoutManager);

                try {

                    AsyncTask<URL, String, List> infoDiscJour = new GetConditionData(db,url,mdp,res_users,"absence.daily", new String[]{"student_id", "status", "date"},
                            "student_id.id", intentId).execute();
                    List ListInfoDiscJour = infoDiscJour.get();


                    for (Map<String, Object> item0 : (List<Map<String, Object>>) ListInfoDiscJour) {

                        statusDisc.add(item0.get("status").toString());
                        date.add(item0.get("date").toString());
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

                statusDiscArray =statusDisc.toArray(new String[statusDisc.size()]);
                dateArray =date.toArray(new String[date.size()]);

                itemDiscJourEleves=new ArrayList<>();
                for(int i=0;i<statusDiscArray.length;i++) {
                    itemDiscJourEleves.add(new ItemDiscJourEleve(
                            statusDiscArray[i].toString(),
                            dateArray[i].toString()));}



                discJourAdapter = new AdapterDiscJourEleve(itemDiscJourEleves, InfoEleve.this);
                rvAbscenceJournaliaireEleve.setAdapter( discJourAdapter);
                rvAbscenceJournaliaireEleve.getAdapter().notifyDataSetChanged();
                rvAbscenceJournaliaireEleve.scheduleLayoutAnimation();

                txtclose.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        myDialog.dismiss();
                    }
                });
                myDialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
                myDialog.show();
            }
        });

        cardSanction.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                RecyclerView rvSanctionsEleve;
                AdapterSanctionsEleve mAdapter;
                ArrayList<ItemSanctionsEleve> itemSanctionsEleve;

                ArrayList<String> sanctions=new ArrayList<>();
                ArrayList<String> nombre=new ArrayList<>();
                TextView txtclose;
                String[] sanctionArray,nombreArray;
                myDialog.setContentView(R.layout.activity_sanction_eleve);
                txtclose =(TextView) myDialog.findViewById(R.id.txtclose);


                rvSanctionsEleve=myDialog.findViewById(R.id.rvSanctionsEleve);
                rvSanctionsEleve.setHasFixedSize(true);
                RecyclerView.LayoutManager layoutManager = new LinearLayoutManager(InfoEleve.this);
                rvSanctionsEleve.setLayoutManager(layoutManager);


                try {

                    AsyncTask<URL, String, List> infoSanctions = new GetConditionData(db,url,mdp,res_users,"student.sanctions", new String[]{"student_id", "sanction", "number"},
                            "student_id.id", intentId).execute();


                    List ListInfoSanctions = infoSanctions.get();
                    for (Map<String, Object> item : (List<Map<String, Object>>) ListInfoSanctions) {

                        sanctions.add(item.get("sanction").toString());
                        nombre.add(item.get("number").toString());
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

                sanctionArray =sanctions.toArray(new String[sanctions.size()]);
                nombreArray =nombre.toArray(new String[nombre.size()]);



                itemSanctionsEleve =new ArrayList<>();
                for(int i=0;i<sanctionArray.length;i++) {
                    itemSanctionsEleve.add(new ItemSanctionsEleve(
                            sanctionArray[i].toString(),
                            nombreArray[i].toString()));}


                mAdapter = new AdapterSanctionsEleve(itemSanctionsEleve, InfoEleve.this);
                rvSanctionsEleve.setAdapter(mAdapter);
                rvSanctionsEleve.getAdapter().notifyDataSetChanged();
                rvSanctionsEleve.scheduleLayoutAnimation();



                txtclose.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        myDialog.dismiss();
                    }
                });
                myDialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
                myDialog.show();
            }
        });

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
            SessionManagement sessionManagement = new SessionManagement(InfoEleve.this);
            sessionManagement.removeSession();
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);
        }else if(id== android.R.id.home){
            this.finish();
        }
        return true;
    }

}
