package com.example.xingxiang25.userprofile;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.EditText;
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

public class MY_PROFILE extends AppCompatActivity {

    private EditText user_name;
    private int userid;
    private EditText date1;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_my__profile);

        userid = getIntent().getExtras().getInt("Userid");
        //String username=getIntent().getExtras().getString("Username");
        String email = getIntent().getExtras().getString("email");
        String gender = getIntent().getExtras().getString("gender");
        String date = getIntent().getExtras().getString("date");
        int weight = getIntent().getExtras().getInt("weight");
        int height = getIntent().getExtras().getInt("height");

        //request the following things with is Userid
        TextView UserID = (TextView) findViewById(R.id.ID);
        user_name = (EditText) findViewById(R.id.name);
        EditText email1 = (EditText) findViewById(R.id.mail);
        EditText gender1 = (EditText) findViewById(R.id.male2);
        EditText weight1 = (EditText) findViewById(R.id.weight);
        EditText height1 = (EditText) findViewById(R.id.height2);
        date1 = (EditText) findViewById(R.id.day2);
        new JSONTask().execute("https://jsonparsingdemo-cec5b.firebaseapp.com/jsonData/moviesDemoItem.txt");


        UserID.setText(Integer.toString(userid));
        //User_name.setText(username,TextView.BufferType.EDITABLE);
        email1.setText(email, TextView.BufferType.EDITABLE);
        gender1.setText(gender, TextView.BufferType.EDITABLE);
        date1.setText(date, TextView.BufferType.EDITABLE);
        weight1.setText(Integer.toString(weight), TextView.BufferType.EDITABLE);
        height1.setText(Integer.toString(height), TextView.BufferType.EDITABLE);


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
                int date=finalObject.getInt("year");
               // String date2=Integer.toString(date);
                //String[] userinfo= new String[2];
                //userinfo[0]=Username;
                //userinfo[1]=date2;*/
                return Username+","+date;
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
            user_name.setText(split[0]);
            date1.setText(split[1]);

        }
    }
}