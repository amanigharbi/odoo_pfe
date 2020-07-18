package com.gestion.ecole.ui.menu.InformationsEleve;

public class ItemSanctionsEleve {
    String tvStatus,tvNombre;

    public ItemSanctionsEleve(String tvStatus, String tvNombre
            ){
        this.tvStatus=tvStatus;
         this.tvNombre=tvNombre;
    }


    public String getTvStatus() {
        return tvStatus;
    }

    public String getTvNombre() {
        return  tvNombre;
    }



}
