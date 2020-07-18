package com.gestion.ecole.ui.menu.EmploisEleve;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.gestion.ecole.R;


public class AdapterDay extends ArrayAdapter {

    private int resource;
    private LayoutInflater layoutInflater;
    private String[] day = new String[]{};

    public AdapterDay(Context context, int resource, String[] objects) {
        super(context, resource, objects);
        this.resource = resource;
        this.day = objects;
        layoutInflater = (LayoutInflater)context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        ViewHolder holder;
        if(convertView == null){
            holder = new ViewHolder();
            convertView = layoutInflater.inflate(resource, null);

            holder.tvDay = (TextView)convertView.findViewById(R.id.tvDay);
            convertView.setTag(holder);
        }else{
            holder = (ViewHolder)convertView.getTag();
        }


        holder.tvDay.setText(day[position]);

        return convertView;
    }

    class ViewHolder{

        private TextView tvDay;
    }
}