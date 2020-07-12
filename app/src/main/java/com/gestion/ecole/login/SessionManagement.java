package com.gestion.ecole.login;

import android.content.Context;
import android.content.SharedPreferences;

public class SessionManagement {

    SharedPreferences sharedPreferences;
    SharedPreferences.Editor editor;
    String SHARED_PREF_NAME = "session";
    String SESSION_MDP = "session_MDP";
    String SESSION_RES_USERS="res_users";
    String SESSION_ID = "ID_user";
    String SESSION_NAME = "name_user";

    String SESSION_EMAIL = "EMAIL";
    String SESSION_DB = "DB";
    String SESSION_URL = "URL";

    public SessionManagement(Context context){
        sharedPreferences = context.getSharedPreferences(SHARED_PREF_NAME,Context.MODE_PRIVATE);
        editor = sharedPreferences.edit();
    }

    public void saveSession(User user){
        String mdp = user.getmdp();
        String  email = user.getEmail();
        String res_users=user.getIdResUsers();
        String id=user.getId();
        String name_parent=user.getName_parent();
        String db=user.getDb();
        String url=user.getUrl();


        editor.putString(SESSION_MDP,mdp).commit();
        editor.putString(SESSION_EMAIL,email).commit();
        editor.putString(SESSION_RES_USERS,res_users).commit();
        editor.putString(SESSION_ID,id).commit();
        editor.putString(SESSION_NAME,name_parent).commit();
        editor.putString(SESSION_DB,db).commit();
        editor.putString(SESSION_URL,url).commit();
    }


    public String getId(){ return sharedPreferences.getString(SESSION_ID, ""); }

    public String getMdp(){
         return sharedPreferences.getString(SESSION_MDP, "");
    }

    public String getNameParent(){
        return sharedPreferences.getString(SESSION_NAME, "");
    }

    public String getSESSION_DB(){
        return sharedPreferences.getString(SESSION_DB,"");
    }
    public String getSESSION_URL(){
        return sharedPreferences.getString(SESSION_URL,"");
    }
    public String getSESSION_RES_USERS(){ return sharedPreferences.getString(SESSION_RES_USERS,""); }

    public void removeSession(){
        editor.clear().commit();
    }
}
