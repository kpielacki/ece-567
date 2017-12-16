package com.example.xingxiang25.userprofile;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class Hazard extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_hazard);
        int userid=getIntent().getExtras().getInt("Userid");
        //using userid to require hazard location and the distance

    }
}
