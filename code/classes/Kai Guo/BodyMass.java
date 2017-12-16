package com.example.xingxiang25.userprofile;

import android.os.Bundle;
import android.support.annotation.IdRes;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.SeekBar;
import android.widget.TextView;

import com.example.xingxiang25.userprofile.server_posts.MobilePost;
import com.example.xingxiang25.userprofile.server_posts.PostData;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.concurrent.ExecutionException;

public class BodyMass extends AppCompatActivity {

    private EditText editText;
    private TextView lenghtText, statusText, idealText, weightText;
    private SeekBar seekBar;
    private RadioGroup radioGroup;
    private boolean isMan = true;
    private double lenght = 175;
    private double weight = 50;
    private double numSteps = 1000;
    private String username;
    private String session_id;
    private String email="admin@gmail.com";
    private RadioGroup.OnCheckedChangeListener radioProcess = new RadioGroup.OnCheckedChangeListener(){
        @Override
        public void onCheckedChanged(RadioGroup group, @IdRes int checkedId) {
            if(checkedId==R.id.man)
                isMan = true;

            else if(checkedId==R.id.woman)
                isMan = false;

            update();
        }
    };

    private SeekBar.OnSeekBarChangeListener seekProcess = new SeekBar.OnSeekBarChangeListener() {
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

    private TextWatcher editProcess = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            try {
                lenght = Double.parseDouble(s.toString())/100.0;
            }

            catch (NumberFormatException e) {
                lenght = 0.0;
            }

            update();
        }

        @Override
        public void afterTextChanged(Editable s) {

        }
    };

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.bodymass_main);

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

        lenghtText = (TextView) findViewById(R.id.length);
        statusText = (TextView) findViewById(R.id.status);
        idealText = (TextView) findViewById(R.id.ideal);
        weightText = (TextView) findViewById(R.id.weight);
        seekBar = (SeekBar) findViewById(R.id.seekBar);
        radioGroup = (RadioGroup) findViewById(R.id.radioGroup);


        seekBar.setOnSeekBarChangeListener(seekProcess);
        radioGroup.setOnCheckedChangeListener(radioProcess);
    }

    private void update() {
        weightText.setText(String.valueOf(weight+" kg"));
        lenghtText.setText(String.valueOf(lenght+" m"));
        int idealMan = (int) (50+2.3*(lenght*100*0.4-60));
        int idealWoman = (int) (45.5+2.3*(lenght*100*0.4-60));
        double vucutKitle = weight/(lenght*lenght);

        if(isMan) {
            idealText.setText(String.valueOf(idealMan));

            if(vucutKitle<=20.7) {
                statusText.setBackgroundResource(R.color.weak);
                statusText.setText(R.string.weak);
            }

            else if(vucutKitle>20.7 && vucutKitle<=26.4) {
                statusText.setBackgroundResource(R.color.normal);
                statusText.setText(R.string.normal);
            }

            else if(vucutKitle>26.4 && vucutKitle<=27.8) {
                statusText.setBackgroundResource(R.color.bitmore);
                statusText.setText(R.string.bitmore);
            }

            else if(vucutKitle>27.8 && vucutKitle<=31.1) {
                statusText.setBackgroundResource(R.color.more);
                statusText.setText(R.string.more);
            }

            else if(vucutKitle>31.1 && vucutKitle<=34.9) {
                statusText.setBackgroundResource(R.color.obese);
                statusText.setText(R.string.obese);
            }

            else {
                statusText.setBackgroundResource(R.color.doctor);
                statusText.setText(R.string.doctor);
            }
        }

        else {
            idealText.setText(String.valueOf(idealWoman));

            if(vucutKitle<=19.1) {
                statusText.setBackgroundResource(R.color.weak);
                statusText.setText(R.string.weak);
            }

            else if(vucutKitle>19.1 && vucutKitle<=25.8) {
                statusText.setBackgroundResource(R.color.normal);
                statusText.setText(R.string.normal);
            }

            else if(vucutKitle>25.8 && vucutKitle<=27.3) {
                statusText.setBackgroundResource(R.color.bitmore);
                statusText.setText(R.string.bitmore);
            }

            else if(vucutKitle>27.3 && vucutKitle<=32.3) {
                statusText.setBackgroundResource(R.color.more);
                statusText.setText(R.string.more);
            }

            else if(vucutKitle>32.3 && vucutKitle<=34.9) {
                statusText.setBackgroundResource(R.color.obese);
                statusText.setText(R.string.obese);
            }

            else {
                statusText.setBackgroundResource(R.color.doctor);
                statusText.setText(R.string.doctor);
            }
        }
    }
}
