package com.gestion.ecole.odoo;


import android.os.AsyncTask;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;


import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.List;

import static com.gestion.ecole.odoo.ConnectionOdoo.uid;
import static java.util.Arrays.asList;

public class GetConnectionData extends AsyncTask<URL,String, List>  {
    static  List ids;
    String table;
    String attr1,attr2,db,url,password;
    String[] fields;


    public GetConnectionData(){
        super();
    };
    public GetConnectionData(String db, String url, String password, String table, String[] fields, String attr1, String attr2){
        this.db=db;
        this.url=url;

        this.password=password;
        this.table=table;
        this.fields=fields;
        this.attr1=attr1;
        this.attr2=attr2;
    }

    @Override
    protected  List doInBackground(URL... urls) {

        try {
            final XmlRpcClient models = new XmlRpcClient() {{
                setConfig(new XmlRpcClientConfigImpl() {{
                    setServerURL(new URL(String.format("%s/xmlrpc/2/object", url)));
                }});
            }};
            models.execute("execute_kw", asList(
                    db, uid, password, table, "check_access_rights", asList("read"),
                    new HashMap() {{
                        put("raise_exception", false);
                    }}
            ));
          ids=asList((Object[])models.execute("execute_kw", asList(
                    db, uid, password, table, "search_read", asList(asList(
                          asList(attr1, "=", attr2)))
                  , new HashMap() {{ put("fields", asList(fields));  }}
                    )));


        } catch (ClassCastException e) {
            e.printStackTrace();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (XmlRpcException e) {
            e.printStackTrace();
        }

        return ids;
    }
}


