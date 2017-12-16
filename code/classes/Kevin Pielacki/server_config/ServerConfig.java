package com.example.xingxiang25.userprofile.server_config;

/**
 * Created by xingxiang25 on 12/8/2017.
 */


public class ServerConfig {

    // SET THIS TO SERVER IP
    private final String SERVER_URL = "http://138.197.80.193/";
    // SET THIS TO PORT SERVER IS LISTENING
    private final int SERVER_PORT = 80;

    public String getServerUrl() {
        return SERVER_URL;
    }

    public int getServerPort() {
        return SERVER_PORT;
    }
}
