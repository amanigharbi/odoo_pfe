package com.gestion.ecole.ui.menu.InformationsEleve;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.view.animation.LayoutAnimationController;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;

import java.util.ArrayList;

public class AdapterInfoEleve extends RecyclerView.Adapter<AdapterInfoEleve.ViewHolder> {

    ArrayList<ItemInfoEleve> list;
    Context context;

    public AdapterInfoEleve(ArrayList<ItemInfoEleve> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_informations_eleve, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
       // LayoutAnimationController animation = AnimationUtils.loadLayoutAnimation(context, R.anim.layoutanim);
        holder.tvNom.setText(list.get(position).getNom());
        holder.tvNomParent.setText(list.get(position).getNomParent());
        holder.tvNomClasse.setText(list.get(position).getNomClasse());

        holder.imgInfoEleve.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_transition));
        holder.RlInfoEleve.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_scale));
    }

    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvNom, tvNomParent,tvNomClasse;
        public RelativeLayout RlInfoEleve;
        public RecyclerView rvInformationsEleve;
        public ImageView imgInfoEleve;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            tvNom = itemView.findViewById(R.id.tvNom);
            tvNomParent = itemView.findViewById(R.id.tvNomParent);
            tvNomClasse = itemView.findViewById(R.id.tvNomClasse);

           imgInfoEleve=itemView.findViewById(R.id.imgInfoEleve);

           RlInfoEleve = itemView.findViewById(R.id.RlInfoEleve);
            rvInformationsEleve=itemView.findViewById(R.id.rvInformationsEleve);

        }
    }
}
