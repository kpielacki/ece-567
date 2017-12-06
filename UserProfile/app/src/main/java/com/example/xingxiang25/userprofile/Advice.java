package com.example.xingxiang25.userprofile;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class Advice extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_advice);
        int userid=getIntent().getExtras().getInt("Userid");
    }
}
