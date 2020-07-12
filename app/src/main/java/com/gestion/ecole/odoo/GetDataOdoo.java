package com.gestion.ecole.odoo;

import android.os.AsyncTask;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import static com.gestion.ecole.odoo.ConnectionOdoo.db;
import static com.gestion.ecole.odoo.ConnectionOdoo.password;
import static com.gestion.ecole.odoo.ConnectionOdoo.url;
import static com.gestion.ecole.odoo.ConnectionOdoo.uid;
import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;

public class GetDataOdoo extends AsyncTask<URL,String, List> {
    static List Resp;
    String table;
    String[] fields;



    public GetDataOdoo(){
        super();
    }

    public GetDataOdoo(String table,String[] fields){
        this.table=table;
        this.fields=fields;

    }


    @Override
    protected List doInBackground(URL... urls) {
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
            Resp = asList((Object[]) models.execute("execute_kw", asList(
                    db, uid, password, table, "search_read",
                    emptyList(),
                    new HashMap() {{
                        put("fields", asList(fields));
                        //put("limit", 5);
                    }})));
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (XmlRpcException e) {
            e.printStackTrace();
        }

        return Resp;
    }

}
