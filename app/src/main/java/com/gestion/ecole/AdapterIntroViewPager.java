package com.gestion.ecole;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.viewpager.widget.PagerAdapter;

import java.util.List;

public class AdapterIntroViewPager extends PagerAdapter {
    Context context;
    List<ScreenItem> mIntegerList;

    public AdapterIntroViewPager(Context context, List<ScreenItem> mIntegerList) {
        this.context = context;
        this.mIntegerList = mIntegerList;
    }

    @NonNull
    @Override
    public Object instantiateItem(@NonNull ViewGroup container, int position) {
        View v = LayoutInflater.from(context).inflate(R.layout.view_intro_screen,null);
        ImageView imgIntro = v.findViewById(R.id.imgIntro);
        TextView textIntro = v.findViewById(R.id.textIntro);
        TextView descIntro =  v.findViewById(R.id.descIntro);

        imgIntro.setImageResource(mIntegerList.get(position).getScreenImg());
       textIntro.setText (mIntegerList.get(position).getTitle());
        descIntro.setText (mIntegerList.get(position).getDescription());

        container.addView(v);

        return v;
    }

    @Override
    public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
        container.removeView((View)object);
    }

    @Override
    public int getCount()
    {
       return mIntegerList.size();
    }

    @Override
    public boolean isViewFromObject(@NonNull View view, @NonNull Object object) {

        return view== object;
    }
}
