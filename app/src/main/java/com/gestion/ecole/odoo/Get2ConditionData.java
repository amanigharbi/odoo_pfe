package com.gestion.ecole.odoo;

import android.os.AsyncTask;

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.List;

import static java.util.Arrays.asList;

public class Get2ConditionData extends AsyncTask<URL,String, List> {
    static  List ids;
    String table;
    String attr1,attr2,attr3,attr4,db,url,uid,password;
    String[] fields;


    public Get2ConditionData(){
        super();
    };
    public Get2ConditionData(String db, String url, String password, String uid,String table, String[] fields,String attr1,String attr2,String attr3,String attr4){
        this.db=db;
        this.url=url;
        this.password=password;
        this.uid=uid;
        this.table=table;
        this.fields=fields;
        this.attr1=attr1;
        this.attr2=attr2;
        this.attr3=attr3;
        this.attr4=attr4;
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
                            asList(attr1, "=", attr2),asList(attr3,"=",attr4)))
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
