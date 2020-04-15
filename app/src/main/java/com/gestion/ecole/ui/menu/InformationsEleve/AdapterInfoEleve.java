package com.gestion.ecole.ui.menu.InformationsEleve;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
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
        holder.tvNom.setText(list.get(position).getNom());
        holder.tvPrenom.setText(list.get(position).getPrenom());
        holder.tvNomParent.setText(list.get(position).getNomParent());
        holder.tvNomClasse.setText(list.get(position).getNomClasse());
    }

    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvNom, tvPrenom, tvNomParent, tvNomClasse;
        public RelativeLayout RlInfoEleve;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            tvNom = itemView.findViewById(R.id.tvNom);
            tvPrenom = itemView.findViewById(R.id.tvPrenom);
            tvNomParent = itemView.findViewById(R.id.tvNomParent);
            tvNomClasse = itemView.findViewById(R.id.tvNomClasse);
            RlInfoEleve = itemView.findViewById(R.id.RlInfoEleve);
        }
    }
}
