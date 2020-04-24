package com.gestion.ecole.ui.menu;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;
import com.gestion.ecole.ui.menu.ContactEnseignant.ContactEnseignant;
import com.gestion.ecole.ui.menu.EmploisEleve.EmploisEleve;
import com.gestion.ecole.ui.menu.InformationsEleve.InformationsEleve;

import java.util.ArrayList;

public class AdapterMenu  extends RecyclerView.Adapter<AdapterMenu.ViewHolder>{
    ArrayList<ItemMenu> list;
    Context context;

    public AdapterMenu(ArrayList<ItemMenu> list, Context context) {
        this.list = list;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_menu, viewGroup, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull final ViewHolder viewHolder, final int i) {
        viewHolder.tvTitle.setText(list.get(i).getTitle());
        viewHolder.tvDesc.setText(list.get(i).getDescription());
        viewHolder.imgArticle.setImageResource(list.get(i).getScreenImg());

        viewHolder.btReadMore.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if(list.get(i).getTitle() == "Informations")
                { v.getContext().startActivity(new Intent(v.getContext(), InformationsEleve.class));}
                   else if (list.get(i).getTitle() == "Contacts")
                    v.getContext().startActivity(new Intent(v.getContext(), ContactEnseignant.class));
                   else if (list.get(i).getTitle() == "Emplois"){
                    v.getContext().startActivity(new Intent(v.getContext(), EmploisEleve.class));

                }
            }
        });




    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public ImageView imgArticle;
        public TextView tvTitle,tvDesc;
        public Button btReadMore;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            imgArticle  = itemView.findViewById(R.id.imgArticle);
            tvTitle     = itemView.findViewById(R.id.tvTitle);
            tvDesc      = itemView.findViewById(R.id.tvDesc);
            btReadMore  = itemView.findViewById(R.id.btReadMore);
        }
    }
}
