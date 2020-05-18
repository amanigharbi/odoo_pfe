package com.gestion.ecole.odoo;

import android.os.AsyncTask;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.List;

import static com.gestion.ecole.odoo.ConnectionOdoo.db;
import static com.gestion.ecole.odoo.ConnectionOdoo.password;
import static com.gestion.ecole.odoo.ConnectionOdoo.uid;
import static com.gestion.ecole.odoo.ConnectionOdoo.url;
import static java.util.Arrays.asList;

public class SetDataOdoo extends AsyncTask<URL,String, Boolean> {
    static Boolean ids;
    String table;
    String[] fields;
    String attr1,attr2,id;

    public SetDataOdoo(String table,String id,String attr1,String attr2){
        this.table=table;
        this.fields=fields;
        this.id=id;
        this.attr1=attr1;
        this.attr2=attr2;
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
                    db, uid, password, table, "write", asList(
                            asList(id)
                    , new HashMap() {{
                        put(attr1, attr2);
                    }}
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

    }}