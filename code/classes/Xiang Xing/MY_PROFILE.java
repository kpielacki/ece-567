package com.example.xingxiang25.userprofile;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.EditText;
import android.widget.TextView;

public class MY_PROFILE extends AppCompatActivity {

    private EditText user_name;
    private int userid;
    private EditText date1;
    private TextView userID;
    private EditText email1;
    private EditText gender1;
    private EditText weight1;
    private EditText height1;
    private String username;
    private String email;
    private String gender;
    private String date;
    private int weight;
    private int height;
    private double bmi;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my__profile);

        userid = getIntent().getExtras().getInt("Userid");
        username = getIntent().getExtras().getString("Username");
        email = getIntent().getExtras().getString("email");
        gender = getIntent().getExtras().getString("gender");
        date = getIntent().getExtras().getString("date");
        weight = getIntent().getExtras().getInt("weight");
        height = getIntent().getExtras().getInt("height");
        bmi = getIntent().getExtras().getDouble("bmi");

        //request the following things with is Userid
        userID = (TextView) findViewById(R.id.ID);
        user_name = (EditText) findViewById(R.id.name);
        email1 = (EditText) findViewById(R.id.mail);
        gender1 = (EditText) findViewById(R.id.male2);
        weight1 = (EditText) findViewById(R.id.weight);
        height1 = (EditText) findViewById(R.id.height2);
        date1 = (EditText) findViewById(R.id.day2);

        userID.setText(Integer.toString(userid));
        user_name.setText(username,TextView.BufferType.EDITABLE);
        //User_name.setText(username,TextView.BufferType.EDITABLE);
        email1.setText(email, TextView.BufferType.EDITABLE);
        gender1.setText(gender, TextView.BufferType.EDITABLE);
        date1.setText(date, TextView.BufferType.EDITABLE);
        weight1.setText(Integer.toString(weight), TextView.BufferType.EDITABLE);
        height1.setText(Integer.toString(height), TextView.BufferType.EDITABLE);


    }


}