package com.gestion.ecole.odoo;

import android.os.AsyncTask;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;

import static com.gestion.ecole.odoo.ConnectionOdoo.db;
import static com.gestion.ecole.odoo.ConnectionOdoo.password;
import static com.gestion.ecole.odoo.ConnectionOdoo.uid;
import static com.gestion.ecole.odoo.ConnectionOdoo.url;
import static java.util.Arrays.asList;

public class DeleteRegIdOdoo  extends AsyncTask<URL,String,Boolean> {
    String table,db,url,uid,password;
    String id;


    public DeleteRegIdOdoo(String db, String url, String password, String uid,String table,String id){
        this.db=db;
        this.url=url;
        this.uid=uid;
        this.password=password;
        this.table=table;
        this.id=id;


    }
    @Override
    protected Boolean doInBackground(URL... urls) {
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
            models.execute("execute_kw", asList(
                    db, uid, password,
                    table, "unlink",
                    asList(asList(id))));

            //Tester si le record existe encore dans la base
            asList((Object[])models.execute("execute_kw", asList(
                    db, uid, password,
                    table, "search",
                    asList(asList(asList("id", "=", id)))
            )));
            return true;
        } catch (ClassCastException e) {
            e.printStackTrace();
            return false;

        } catch (MalformedURLException e) {
            e.printStackTrace();
            return false;
        } catch (XmlRpcException e) {
            e.printStackTrace();
            return false;

        }
    }
}
