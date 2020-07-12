package com.gestion.ecole.ui.menu.ContactEnseignant;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.AnimationUtils;
import android.view.animation.LayoutAnimationController;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.gestion.ecole.R;

import java.util.ArrayList;

public class AdapterContactEns  extends RecyclerView.Adapter<AdapterContactEns.ViewHolder>{
    ArrayList<ItemEnseignant> list;
    Context context;

    public AdapterContactEns(ArrayList<ItemEnseignant> list, Context context) {
        this.list = list;
        this.context = context;
    }
    public AdapterContactEns(ArrayList<ItemEnseignant> list) {
        this.list = list;

    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup viewGroup, int i) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_contact_enseignant, viewGroup, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder viewHolder, int i) {
        LayoutAnimationController animation = AnimationUtils.loadLayoutAnimation(context, R.anim.layoutanim);
        viewHolder.tvNomPrenom.setText(list.get(i).getNomPrenom());
        viewHolder.tvEmail.setText(list.get(i).getEmail());
        viewHolder.tvNum.setText(list.get(i).getNum());


        viewHolder.btnSenEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String receiveEmaiil = viewHolder.tvEmail.getText().toString();
                String [] split=receiveEmaiil.split(",");
                System.out.println("hello "+split);
                String Subject ="Renseignement";
                Intent intent= new Intent(Intent.ACTION_SEND);

                intent.putExtra(Intent.EXTRA_EMAIL,split);
                intent.putExtra(Intent.EXTRA_SUBJECT,Subject);
                intent.putExtra(Intent.EXTRA_TEXT,"message body");
                intent.setType("message/rfc822");
                context.startActivity(Intent.createChooser(intent,"Choose an email client"));
            }
        });

        viewHolder.rl1.setLayoutAnimation(animation);
    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public ImageView imgEnseignant;
        public TextView tvNomPrenom,tvEmail,tvNum;
        public RelativeLayout rl1;
        Button btnSenEmail;


        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            imgEnseignant  = itemView.findViewById(R.id.imgEnseignant);
            tvNomPrenom     = itemView.findViewById(R.id.tvNomPrenom);
            tvEmail      = itemView.findViewById(R.id.tvEmail);
            tvNum      = itemView.findViewById(R.id.tvNum);
            btnSenEmail = itemView.findViewById(R.id.btnContact);
            rl1         = itemView.findViewById(R.id.rl1);
        }
    }
}