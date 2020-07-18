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

public class CreateRegId extends AsyncTask<URL,String,Boolean> {
    String table;
    String db,url,uid,password;
    String field1,field2,val1,val2;

    public CreateRegId(String db, String url, String password, String uid,String table,String field1,String val1,String field2,String val2){
        this.db=db;
        this.url=url;
        this.uid=uid;
        this.password=password;
        this.table=table;
        this.field1=field1;
        this.val1=val1;
        this.field2=field2;
        this.val2=val2;


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
                    table, "create",
                    asList(new HashMap() {{ put(field1,val1);
                                            put(field2,val2);}})
            ));
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
