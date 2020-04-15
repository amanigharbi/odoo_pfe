package com.gestion.ecole.odoo;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static java.util.Collections.emptyMap;


public class ConnectionOdoo extends AsyncTask<URL,String,String> {

    static String db;
    static String username;
    static String password;
    static String url;
    static TextView txt;
    static int uid=0;
    static List Resp;
    static Context app;

    public ConnectionOdoo(String db, int uid, String password){
        this.db=db;
        this.uid=uid;
        this.password=password;
    }

    public ConnectionOdoo(String db, String username, String password, String url, Context app){
        this.db=db;
        this.username=username;
        this.password=password;
        this.url=url;
        // this.txt=txt;
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

            System.out.println("admin : "+ uid);



               // Toast.makeText(app, "1", Toast.LENGTH_LONG).show();
               /*  models.execute("execute_kw", asList(
                        db, uid, password, "res.partner", "check_access_rights", asList("read"),
                        new HashMap() {{
                            put("raise_exception", false);
                        }}
                ));
                //Toast.makeText(app, "2", Toast.LENGTH_LONG).show();
               Resp = asList((Object[]) models.execute("execute_kw", asList(
                        db, uid, password, "res.partner", "search_read",
                  */      /*emptyList()*//*asList(asList(
                                asList("is_company", "=", true),
                                asList("customer", "=", true))),
                      */  //emptyList(),
            //a {{
                        /*new HashMap() {{
                            put("fields", asList("name"));
                            put("limit", 5);
                        }})));*/





            /*final List ids=asList((Object[]) models.execute(
                    "execute_kw",asList(
                            db,uid,password,"product.product","search")));
*/
            /*return asList((Object[]) models.execute(
                     "execute_kw",asList(
                             db,uid,password,"product.product","read",
                             new HashMap(){{
                                 put("fields",asList("name"));
                             }}
                                     )
                             )
                     ).toString();
*/
            //JSONArray jspn;
            // (Map<String,Map<String,Object>>)
            // HashMap <String,Map<String,Object>> a = new HashMap();
            //new Map (Map<String,Map<String,Object>>) =
            //  Map<String, Map<String, Object>> Responce =(Map<String, Map<String, Object>>)

            //}}
            /*ByteArrayOutputStream bos = new ByteArrayOutputStream();
            XMLEncoder xmlEncoder = new XMLEncoder(bos);
            xmlEncoder.writeObject(map);
            xmlEncoder.flush();

            String serializedMap = bos.toString()
            String X="";*/

          /*  Iterator iterator = a.entrySet().iterator();
            while(iterator.hasNext()){
                Map.Entry map = (Map.Entry) iterator.next();
                X+="cle:"+map.getKey()+"val:"+map.getValue();
            }*/
            /*String x = "";
            Iterator<String> iter = Resp.iterator();
            while (iter.hasNext()) {
                x += "- " + iter.next();
            }*/
            //for(I)
            //return Resp.toString();
            return "Connected";//Resp.toString();

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
