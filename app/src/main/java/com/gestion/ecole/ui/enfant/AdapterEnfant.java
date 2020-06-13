package com.gestion.ecole.ui.enfant;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;
import com.gestion.ecole.ui.menu.ContactEnseignant.ContactEnseignant;
import com.gestion.ecole.ui.menu.EmploisEleve.EmploisEleve;
import com.gestion.ecole.ui.menu.InformationsEleve.InformationsEleve;

import java.util.ArrayList;

public class AdapterEnfant extends RecyclerView.Adapter<AdapterEnfant.ViewHolder> {
    ArrayList<ItemEnfant> list;
    Context context;
    Fragment fragment;
    public AdapterEnfant(ArrayList<ItemEnfant> list, Context context) {
        this.list = list;
        this.context = context;
    }
    public AdapterEnfant(Fragment fragment){
        this.fragment=fragment;
    }

    @NonNull
    @Override
    public AdapterEnfant.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_enfant_consulter, parent, false);
        return new AdapterEnfant.ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull AdapterEnfant.ViewHolder holder, int position) {
        // LayoutAnimationController animation = AnimationUtils.loadLayoutAnimation(context, R.anim.layoutanim);
        holder.tvNom.setText(list.get(position).getNom());
        holder.tvNomParent.setText(list.get(position).getNomParent());
        holder.tvNomClasse.setText(list.get(position).getNomClasse());
        holder.idEnfant.setText(list.get(position).getIdEnfant());

        holder.imgInfoEleve.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_transition));
        holder.RlEnfant.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_scale));

        holder.btnConsulter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = ((Activity) context).getIntent();
                Intent i1,i2,i3;
                String var =intent.getStringExtra("1");
                String id=holder.idEnfant.getText().toString();
                System.out.println("no "+id);
                if(var .equals("Disciplines")){
                    i1=new Intent(v.getContext(), InformationsEleve.class);
                    i1.putExtra("id",id);
                    v.getContext().startActivity(i1);
               }
                else if(var .equals("Emplois")){
                    i2=new Intent(v.getContext(), EmploisEleve.class);
                    i2.putExtra("id",id);
                    v.getContext().startActivity(i2);
                    //v.getContext().startActivity(new Intent(v.getContext(), EmploisEleve.class));
                }
                else if(var .equals("Contacts")){
                    i3=new Intent(v.getContext(), ContactEnseignant.class);
                    i3.putExtra("id",id);
                    v.getContext().startActivity(i3);
                    //v.getContext().startActivity(new Intent(v.getContext(), ContactEnseignant.class));
                }

            }
    });
    }
    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder  {

        public TextView tvNom, tvNomParent,tvNomClasse,idEnfant;
        public Button btnConsulter;
        public RelativeLayout RlEnfant;

        public ImageView imgInfoEleve;
        FragmentManager manager;
        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            idEnfant = itemView.findViewById(R.id.idEnfant);
            idEnfant.setVisibility(itemView.INVISIBLE);
            tvNom = itemView.findViewById(R.id.tvNom);
            tvNomParent = itemView.findViewById(R.id.tvNomParent);
            tvNomClasse = itemView.findViewById(R.id.tvNomClasse);
            btnConsulter= itemView.findViewById(R.id.btnConsulter);

            imgInfoEleve=itemView.findViewById(R.id.imgInfoEleve);

            RlEnfant = itemView.findViewById(R.id.RlEnfant);


    }}}

