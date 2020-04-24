package com.gestion.ecole.ui.menu.InformationsEleve;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;

import java.util.ArrayList;

public class AdapterDesciplineEleve extends RecyclerView.Adapter<AdapterDesciplineEleve.ViewHolder> {
    ArrayList<ItemDesciplineEleve> list;
    Context context;

    public AdapterDesciplineEleve(ArrayList<ItemDesciplineEleve> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public AdapterDesciplineEleve.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_descipline_eleve, parent, false);
        return new AdapterDesciplineEleve.ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.tvNomMatiere.setText(list.get(position).getNomMatiere());
        holder.tvDateHeure.setText(list.get(position).getDateHeure());
        holder.tvStatus.setText(list.get(position).getSatus());
        holder.RlDescEleve.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_scale));
        holder.imgInfoDescipline.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_transition));
    }


    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvNomMatiere,tvDateHeure,tvStatus;
        public RelativeLayout RlDescEleve;
        public RecyclerView rvDesciplineEleve;
        public ImageView imgInfoDescipline;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);


            tvNomMatiere = itemView.findViewById(R.id.tvNomMatiere);
            tvDateHeure = itemView.findViewById(R.id.tvDateHeure);
            tvStatus = itemView.findViewById(R.id.tvStatus);

            imgInfoDescipline=itemView.findViewById(R.id.imgInfoDescipline);

            RlDescEleve = itemView.findViewById(R.id.RlDescEleve);
            rvDesciplineEleve=itemView.findViewById(R.id.rvDesciplineEleve);

        }
    }
}
