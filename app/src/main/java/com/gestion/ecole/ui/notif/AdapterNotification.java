package com.gestion.ecole.ui.notif;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;

import java.util.ArrayList;

public class AdapterNotification extends RecyclerView.Adapter<AdapterNotification.ViewHolder> {
    ArrayList<ItemNotification> list;
    Context context;


    public AdapterNotification(ArrayList<ItemNotification> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public AdapterNotification.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_historique_notification, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull AdapterNotification.ViewHolder holder, int position) {
        holder.titre.setText(list.get(position).getTitreNotif());
        holder.notif_message.setText(list.get(position).getNotif_message());


        holder.RlNotification.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_transition));
    }

    @Override
    public int getItemCount() {
        return list.size();}

    public class ViewHolder extends RecyclerView.ViewHolder {
        public TextView notif_message, titre;
        public RelativeLayout RlNotification;
        public RecyclerView rvNotification;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            titre = itemView.findViewById(R.id.titre);
            notif_message = itemView.findViewById(R.id.notif_message);

            RlNotification = itemView.findViewById(R.id.RlNotification);

            rvNotification = itemView.findViewById(R.id.rvNotification);
        }
    }
}
