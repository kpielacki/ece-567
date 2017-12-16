package com.example.xingxiang25.userprofile;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

import cn.finalteam.okhttpfinal.OkHttpFinal;
import cn.finalteam.okhttpfinal.OkHttpFinalConfiguration;

public class Findlocation extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.findlocation);
        OkHttpFinalConfiguration.Builder builder = new OkHttpFinalConfiguration.Builder();
        OkHttpFinal.getInstance().init(builder.build());
    }

    @Override
    protected void onStart() {
        super.onStart();
        //google API返回的经纬度结果推荐去http://www.gpsspg.com/maps.htm查看具体位置，防止国内被混淆

        //开启位置监听
        AlxLocationManager.onCreateGPS(getApplication());

        final TextView tv_latitude = (TextView) findViewById(R.id.tv_latitude);
        final TextView tv_longitude = (TextView) findViewById(R.id.tv_longitude);
        final TextView tv_accuracy = (TextView) findViewById(R.id.tv_accuracy);
        final TextView tv_time = (TextView) findViewById(R.id.tv_time);
        final TextView tv_data = (TextView) findViewById(R.id.tv_data);
        final Handler handler = new Handler();
        //每隔2s更新一下经纬度结果
        new Timer().scheduleAtFixedRate(new TimerTask() {//每秒钟检查一下当前位置
            @Override
            public void run() {
                handler.post(new Runnable() {
                    @Override
                    public void run() {
                        tv_latitude.setText(String.valueOf(MyLocation.getInstance().latitude));
                        tv_longitude.setText(String.valueOf(MyLocation.getInstance().longitude));
                        tv_accuracy.setText(String.valueOf(MyLocation.getInstance().accuracy));
                        if(MyLocation.getInstance().updateTime != 0)tv_time.setText(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date(MyLocation.getInstance().updateTime)));
                        if(AlxLocationManager.getInstance()==null)return;
                        String json = AlxLocationManager.getInstance().dataJson;
                        if(TextUtils.isEmpty(json))return;
                        json = json.replaceAll("\\},","},\n");
                        tv_data.setText(json);
                    }
                });
            }
        },0,2000);
    }

    @Override
    protected void onStop() {
        super.onStop();
        AlxLocationManager.stopGPS();
    }
}
