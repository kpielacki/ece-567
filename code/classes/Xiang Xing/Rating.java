package com.example.xingxiang25.userprofile;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;

public class Rating extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rating);
        int userid=getIntent().getExtras().getInt("Userid");


    }
}
