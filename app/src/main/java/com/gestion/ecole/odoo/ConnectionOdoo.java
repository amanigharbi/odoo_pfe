package com.gestion.ecole.odoo;

import android.content.Context;
import android.os.AsyncTask;


import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.net.MalformedURLException;
import java.net.URL;


import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static java.util.Collections.emptyMap;


public class ConnectionOdoo extends AsyncTask<URL,String,String> {

    static String db;
    static String username;
    static String password;
    static String url;
    static int uid=0;

    static Context app;


    public ConnectionOdoo(String db, String username, String password, String url, Context app){
        this.db=db;
        this.username=username;
        this.password=password;
        this.url=url;
        this.app=app;
    }

    @Override
    protected String doInBackground(URL... urls) {

        try{
            final XmlRpcClient client = new XmlRpcClient();
            final XmlRpcClientConfigImpl common_config = new XmlRpcClientConfigImpl();

            common_config.setServerURL(
                    new URL(String.format("%s/xmlrpc/2/common", url)));
            client.execute(common_config, "version", emptyList());
                 System.out.println("connection");


                  uid = (int)client.execute(
                    common_config, "authenticate", asList(
                            db, username, password, emptyMap()));


            return "Connected" ;

       } catch( ClassCastException e) {
            return e.getMessage();
        }catch
         (XmlRpcException e) {
            e.printStackTrace();
            return e.getMessage();
        }catch (MalformedURLException e) {

            return e.getMessage();
        }
    }

    @Override
    protected void onPostExecute(String s) {
      //  super.onPostExecute(s);
    //    if(s.equals("Connected")){
      //    Toast.makeText(app, s, Toast.LENGTH_LONG).show();
      //  }else{
      //      Toast.makeText(app, "not connected", Toast.LENGTH_LONG).show();
      //  }


    }



}
