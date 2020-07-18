package com.gestion.ecole.ui.menu.EmploisEleve;

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

public class AdapterDayDetails extends  RecyclerView.Adapter<AdapterDayDetails.ViewHolder>{
    ArrayList<ItemDayDetails> list;
    Context context;

    public AdapterDayDetails(ArrayList<ItemDayDetails> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_emplois_details, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.tvTime.setText(list.get(position).getTime());
        holder.tvSubject.setText(list.get(position).getSubject());
        holder.tvTeacher.setText(list.get(position).getTeacher());



        holder.RlDetailsEmplois.setAnimation(AnimationUtils.loadAnimation(context,R.anim.layout_anim_transition));
    }

    @Override
    public int getItemCount() {
        return list.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder {

        public TextView tvTime, tvSubject,tvTeacher;
        public RelativeLayout RlDetailsEmplois;


        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            tvTime = itemView.findViewById(R.id.tvTime);
            tvSubject = itemView.findViewById(R.id.tvSubject);
            tvTeacher = itemView.findViewById(R.id.tvTeacher);



            RlDetailsEmplois=itemView.findViewById(R.id.RlDetailsEmplois);

        }
    }
}