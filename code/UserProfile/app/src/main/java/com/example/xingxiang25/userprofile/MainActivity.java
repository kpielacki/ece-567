package com.example.xingxiang25.userprofile;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button myprofilebtn=(Button) findViewById(R.id.button1);
        Button caloriesbtn=(Button) findViewById(R.id.button2);
        Button Hazardbtn=(Button) findViewById(R.id.button3);
        Button Ratingbtn=(Button) findViewById(R.id.button4);
        Button Advisebtn=(Button) findViewById(R.id.button5);

        final int UserId=1;//just for temporary use, later should be passed from the login processs
        final String Username="sam";
        final String email= "xx.gmail.com";
        final String gender="male";
        final String date="2007-2-1";
        final int weight= 80;
        final int height =180;
        //url connection in the main menu



        myprofilebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent myprofile=new Intent(getApplicationContext(),MY_PROFILE.class);
                myprofile.putExtra("Userid", UserId);
                myprofile.putExtra("Username",Username);
                myprofile.putExtra("email",email);
                myprofile.putExtra("gender",gender);
                myprofile.putExtra("date",date);
                myprofile.putExtra("weight",weight);
                myprofile.putExtra("height",height);

                startActivity(myprofile);
            }
        });
        caloriesbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent calories= new Intent(getApplicationContext(),caloryandexercies.class);
                calories.putExtra("Userid", UserId);
                startActivity(calories);
            }
        });
        Hazardbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent Hazard= new Intent(getApplicationContext(), Hazard.class);
                Hazard.putExtra("Userid", UserId);
                startActivity(Hazard);
            }
        });
        Ratingbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent rating= new Intent(getApplicationContext(),Rating.class);
                rating.putExtra("Userid", UserId);
                startActivity(rating);
            }
        });
        Advisebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent advising= new Intent(getApplicationContext(),Advice.class);
                advising.putExtra("Userid", UserId);
                startActivity(advising);
            }
        });
    }
}
