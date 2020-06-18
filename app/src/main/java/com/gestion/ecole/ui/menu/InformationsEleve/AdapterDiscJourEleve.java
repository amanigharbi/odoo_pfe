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

public class AdapterDiscJourEleve extends RecyclerView.Adapter<AdapterDiscJourEleve.ViewHolder>{
    ArrayList<ItemDiscJourEleve> list;
    Context context;

    public AdapterDiscJourEleve(ArrayList<ItemDiscJourEleve> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_discipline_journaliaire_enfant, parent, false);
        return new ViewHolder(v);
    }


    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        // LayoutAnimationController animation = AnimationUtils.loadLayoutAnimation(context, R.anim.layoutanim);
        holder.tvStatus.setText(list.get(position).getTvStatus());
        holder.tvDate.setText(list.get(position).getTvDate());


        holder.imgInfoEleve.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_transition));
        holder.RlDiscJourEleve.setAnimation(AnimationUtils.loadAnimation(context, R.anim.layout_anim_scale));
    }

    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvStatus, tvDate;
        public RelativeLayout RlDiscJourEleve;
        public ImageView imgInfoEleve;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            tvStatus = itemView.findViewById(R.id.tvStatus);
            tvDate = itemView.findViewById(R.id.tvdate);


            imgInfoEleve=itemView.findViewById(R.id.imgInfoEleve);

            RlDiscJourEleve = itemView.findViewById(R.id.RlDiscJourEleve);


        }
    }
}
