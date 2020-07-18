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

public class AdapterSanctionsEleve extends RecyclerView.Adapter<AdapterSanctionsEleve.ViewHolder> {

    ArrayList<ItemSanctionsEleve> list;
    Context context;

    public AdapterSanctionsEleve(ArrayList<ItemSanctionsEleve> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_sanctions_eleve, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.tvStatus.setText(list.get(position).getTvStatus());
        holder.tvNombre.setText(list.get(position).getTvNombre());


        holder.imgInfoEleve.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_transition));
        holder.RlSanctionsEleve.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_scale));
    }

    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvStatus, tvNombre;
        public RelativeLayout RlSanctionsEleve;
        public ImageView imgInfoEleve;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            tvStatus = itemView.findViewById(R.id.tvStatus);
            tvNombre = itemView.findViewById(R.id.tvNombre);


           imgInfoEleve=itemView.findViewById(R.id.imgInfoEleve);

            RlSanctionsEleve = itemView.findViewById(R.id.RlSanctionsEleve);


        }
    }
}
