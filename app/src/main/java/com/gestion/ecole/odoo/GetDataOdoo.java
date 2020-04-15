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
import static com.gestion.ecole.odoo.ConnectionOdoo.url;
import static com.gestion.ecole.odoo.ConnectionOdoo.uid;
import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;

public class GetDataOdoo extends AsyncTask<URL,String, List> {
    static List Resp;
    String table;
    String str="";
    String[] fields;
    String[][] condition;

    public GetDataOdoo(){
        super();
    }

    public GetDataOdoo(String table, String[] fields,String[][] condition){
        this.table=table;
        this.fields=fields;
        this.condition=condition;
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
                    db, uid, password, table, "search_read",listConditions(condition),
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
    public List listConditions(String[][] conditions){
        if(conditions==null) return emptyList();
        if(conditions.length==1) return asList(asList(asList(conditions[0])));
        if(conditions.length==2) return asList(asList(asList(conditions[0]),asList(conditions[1])));
        if(conditions.length==3) return asList(asList(asList(conditions[0]),asList(conditions[1]),asList(conditions[2])));
        if(conditions.length==4) return asList(asList(asList(conditions[0]),asList(conditions[1]),asList(conditions[2]),asList(conditions[3])));
      return emptyList();
    }
}
