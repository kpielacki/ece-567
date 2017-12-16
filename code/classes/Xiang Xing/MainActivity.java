package com.example.xingxiang25.userprofile;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;

import com.example.xingxiang25.userprofile.server_posts.MobilePost;
import com.example.xingxiang25.userprofile.server_posts.PostData;
import com.example.xingxiang25.userprofile.view.stepcounter;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

//import com.alibaba.fastjson.JSONException;
//import com.alibaba.fastjson.JSONObject;
public class MainActivity extends AppCompatActivity {

    private String username;
    private String session_id;
    private String email;
    private String gender;
    private String date;
    private int weight;
    private int height;
    private double bmi;
    private int userid;
    private String test;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button myprofilebtn=(Button) findViewById(R.id.button1);
        Button caloriesbtn=(Button) findViewById(R.id.button2);
        Button Hazardbtn=(Button) findViewById(R.id.button3);
        Button Ratingbtn=(Button) findViewById(R.id.button4);
        Button Advisebtn=(Button) findViewById(R.id.button5);

        username = "";
        userid=-1;
        //primary key
        email = "admin@gmail.com";
        session_id="temporary";
        gender = "";
        date = "";
        weight = 0;
        height = 0;
        bmi = 0;
        test="";

        int try_count=0;
        while (try_count<3) {
            JSONObject jsoninfo = new JSONObject();

            try {
                jsoninfo.put("email", email);
                jsoninfo.put("session_id", session_id);
                PostData profilepost = new PostData("mobile/getprofile/", jsoninfo.toString(), 0);
                MobilePost getprofile = new MobilePost();

                getprofile.execute(profilepost).get();
               // sleep(500);

                JSONObject profileResponse = new JSONObject(profilepost.resp_msg.replace("\n", ""));
                username = profilepost.resp_msg;

                boolean request_success = profileResponse.getBoolean("success");
                String profilemessage = profileResponse.getString("msg");
                if (request_success) {
                    gender = profileResponse.getString("gender");
                    weight = profileResponse.getInt("weight");
                    height = profileResponse.getInt("height");
                    date = profileResponse.getString("birthday");
                    bmi = profileResponse.getDouble("bmi");
                    userid = profileResponse.getInt("userid");
                    username = profileResponse.getString("username");
                    break;
                }
            } catch (JSONException e) {
                //  new RuntimeException("No user info found, key may be not properly passed or wrong");
                try_count++;

            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }


        }


        myprofilebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent myprofile=new Intent(getApplicationContext(),MY_PROFILE.class);
                myprofile.putExtra("Userid",userid);
                myprofile.putExtra("Username", username);
                myprofile.putExtra("email", email);
                myprofile.putExtra("gender", gender);
                myprofile.putExtra("date", date);
                myprofile.putExtra("weight", weight);
                myprofile.putExtra("height", height);
                myprofile.putExtra("bmi",bmi);

                startActivity(myprofile);
            }
        });

        caloriesbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent calories= new Intent(getApplicationContext(),stepcounter.class);
                calories.putExtra("Userid", userid);
                startActivity(calories);
            }
        });
        Hazardbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Intent MapsActivity= new Intent(getApplicationContext(), MapsActivity.class);
                MapsActivity.putExtra("Userid", userid);
                MapsActivity.putExtra("email",email);
                startActivity(MapsActivity);
            }
        });
        Ratingbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent rating= new Intent(getApplicationContext(),Calorie.class);
                rating.putExtra("count", 50);
                rating.putExtra("extra", 60);
                rating.putExtra("height",height);

                startActivity(rating);
            }
        });
        Advisebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent location= new Intent(getApplicationContext(),Findlocation.class);
                location.putExtra("Userid", userid);
                startActivity(location);
            }
        });
    }
}
