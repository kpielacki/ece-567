package com.example.xingxiang25.userprofile;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class caloryandexercies extends AppCompatActivity {

    private int userid;
    private int steps=0;
    private TextView username_textview;
    private TextView steps_textview;
    private TextView energy;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_caloryandexercies);
        //get userid from main
        userid = getIntent().getExtras().getInt("Userid");
        username_textview = (TextView) findViewById(R.id.Username);
        steps_textview = (TextView) findViewById(R.id.in_step);
        energy = (TextView) findViewById(R.id.in_energy);
                new JSONTask().execute("https://jsonparsingdemo-cec5b.firebaseapp.com/jsonData/moviesData.txt");
        //request the info from the database and display
        //require step, energy and average energy consumption of this week
    }

    public class JSONTask extends AsyncTask<String, String, String> {

        @Override
        protected String doInBackground(String...params) {
            HttpURLConnection main_connection = null;
            BufferedReader bufferedReader = null;
            try {

                URL url = new URL(params[0]);
                main_connection = (HttpURLConnection) url.openConnection();
                main_connection.connect();
                InputStream inputStream = main_connection.getInputStream();
                bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                StringBuffer stringBuffer = new StringBuffer();

                String line = "";

                while ((line = bufferedReader.readLine()) != null) {
                    stringBuffer.append(line);

                    //User_name.setText(stringBuffer.toString(),TextView.BufferType.EDITABLE);
                }
                String finalJson= stringBuffer.toString();
                JSONObject parentObject=new JSONObject(finalJson);
                JSONArray parentArray= parentObject.getJSONArray("movies");
                JSONObject finalObject= parentArray.getJSONObject(0);
                String Username=finalObject.getString("movie");
                for(int i=0; i<parentArray.length();i++){
                    JSONObject iterObject= parentArray.getJSONObject(i);
                    steps+=iterObject.getInt("year");
                }
                steps=steps/(parentArray.length());
                return Username+","+steps;



            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            } finally {
                if (main_connection != null) {
                    main_connection.disconnect();
                }
                try {
                    if (bufferedReader != null) {
                        bufferedReader.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return null;
        }


        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            String[] split=result.split(",");

            username_textview.setText(split[0].toString());
            steps_textview.setText(split[1].toString());
            int energy1=Integer.parseInt(split[1]);
            energy1*=0.04;
            String finalenergy=Integer.toString(energy1);
            energy.setText(finalenergy.toString());

        }
    }
}
