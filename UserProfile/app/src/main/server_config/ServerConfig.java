package server_config;


public class ServerConfig {

    // SET THIS TO SERVER IP
    private final String SERVER_URL = "http://127.0.0.1/";
    // SET THIS TO PORT SERVER IS LISTENING
    private final int SERVER_PORT = 80;

    public String getServerUrl() {
        return SERVER_URL;
    }

    public int getServerPort() {
        return SERVER_PORT;
    }
}
