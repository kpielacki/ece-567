package com.example.xingxiang25.userprofile;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;

import com.example.xingxiang25.userprofile.server_posts.MobilePost;
import com.example.xingxiang25.userprofile.server_posts.PostData;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

public class Calorie extends AppCompatActivity {

    private int extra=1;
    private int notHere = 0;
    private EditText editText, editText2;
    private TextView lenghtText, statusText, weightText, bravoText;
    private SeekBar seekBar;
    private double lenght = 175;
    private double weight = 50;
    private double numSteps = 1000;
    private String username;
    private String session_id;
    private String email="admin@gmail.com";
    private String gender;
    private String date;
    private int height;
    private double bmi;
    private int userid;
    private  double calory;
    private double health_index=6.7;




    private SeekBar.OnSeekBarChangeListener seekBarChangeListener = new SeekBar.OnSeekBarChangeListener(){
        @Override

        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            weight = 50 + progress;
            update();
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {

        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {

        }
    };

    private TextWatcher textWatcher = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            try {
                lenght = Integer.parseInt(s.toString());
            }

            catch (NumberFormatException e) {
                lenght = 0;
            }

            update();
        }

        @Override
        public void afterTextChanged(Editable s) {

        }
    };

    private TextWatcher textWatcher2 = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            try {
                notHere = Integer.parseInt(s.toString());
            }

            catch (NumberFormatException e) {
                notHere = 0;
            }

            update();
        }

        @Override
        public void afterTextChanged(Editable s) {

        }
    };

    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.calorie_main);
        Button bodybtn=(Button) findViewById(R.id.body);
        bodybtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent body=new Intent(getApplicationContext(),BodyMass.class);
                startActivity(body);
            }
        });
        int try_count=0;
        while (try_count<3){
            JSONObject jsoninfo = new JSONObject();

            try {
                jsoninfo.put("email", email);
                jsoninfo.put("session_id", "");
                PostData profilepost = new PostData("mobile/getactivity/", jsoninfo.toString(), 0);
                MobilePost getprofile = new MobilePost();

                getprofile.execute(profilepost).get();
                // sleep(500);

                JSONObject profileResponse = new JSONObject(profilepost.resp_msg.replace("\n", ""));
                username = profilepost.resp_msg;

                boolean request_success = profileResponse.getBoolean("success");
                String profilemessage = profileResponse.getString("msg");
                if (request_success) {

                    numSteps=profileResponse.getDouble("steps");
                    weight=profileResponse.getDouble("weight");
                    lenght=profileResponse.getDouble("height");


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
        Bundle extras = getIntent().getExtras();


        lenghtText = (TextView) findViewById(R.id.length);
        weightText = (TextView) findViewById(R.id.weight);
        statusText = (TextView) findViewById(R.id.status);
        seekBar = (SeekBar) findViewById(R.id.seekBar);
        editText2 = (EditText) findViewById(R.id.editText2);
        bravoText = (TextView) findViewById(R.id.bravo);



        editText2.addTextChangedListener(textWatcher2);
        seekBar.setOnSeekBarChangeListener(seekBarChangeListener);

        String sport = getResources().getString(R.string.sport);
        statusText.setText(sport);
        update();

    }

    private void update() {
        weightText.setText(String.valueOf(weight+" kg"));
        lenghtText.setText(String.valueOf(lenght+" cm"));

        String nonStep = getResources().getString(R.string.nonstep);
        String extraString = getResources().getString(R.string.extra);
        String stepString = getResources().getString(R.string.steps);

        double perCm = ((weight*1.256635)/1.609344)/100000;
        double stepLenght = (lenght*42)/100;
        double perStep = perCm*stepLenght;
        double burnCalorie = 0.0;

        if(notHere>0)
            burnCalorie = perStep*(numSteps+notHere);
        else
            burnCalorie = perStep*numSteps;

        if(burnCalorie>=0 && burnCalorie<1)
            statusText.setText(nonStep);

        else if(burnCalorie>=1)
            statusText.setText(String.format("%.2f", burnCalorie)+" cal");

        if(extra>0)
            bravoText.setText("Your overall health rating is "+ health_index +" based on your previous preformance");
    }
}
