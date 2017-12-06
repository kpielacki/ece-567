package server_posts;

import android.os.AsyncTask;
import server_config.ServerConfig;
import java.lang.Integer;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;


public class MobilePost extends AsyncTask<PostData, Integer, Boolean> {

    // Pull server configuration information
    private final static ServerConfig config = new ServerConfig();

    // Supported content types to post data
    private enum ContentType {
        JSON, TXT, CSV
    }

    // Return network error message templates
    private final String MOBILE_ERROR_RESPONSE = "{\"error\": \"%s\"}";

    // Exception message templates
    private final String BAD_URL = "Malformed URL: %s";
    private final String BAD_CONTENT_TYPE = "Unsupported content type: %d";

    private boolean success = false;

    // Sends HTTP POST request with postString as data to server/url_str with
    // content type content_type_in
    @Override
    protected Boolean doInBackground(PostData... params) {
        // Pull POST properties from passed param
        String url_str = params[0].getUrlString();
        String postString = params[0].getPostString();
        int content_type_in = params[0].getContentType();

        byte[] postData = postString.getBytes(StandardCharsets.UTF_8);
        int postDataLength = postData.length;

        // Set content type
        String content_type_str;
        if (content_type_in == ContentType.JSON.ordinal()) {
            content_type_str = "application/json";
        } else if (content_type_in == ContentType.TXT.ordinal()) {
            content_type_str = "text/plain";
        } else if (content_type_in == ContentType.CSV.ordinal()) {
            content_type_str = "text/csv";
        } else {
            throw new java.lang.Error(String.format(BAD_CONTENT_TYPE, content_type_in));
        }

        // Send and receive data
        try {
            URL url = new URL(config.getServerUrl() + url_str);

            // Start HTTP POST connection
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);

            connection.setDoOutput(true);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", content_type_str);
            connection.setRequestProperty("charset", "UTF-8");
            connection.setRequestProperty("Content-Length", Integer.toString(postDataLength));

            // SESSION COOKE FOR FUTURE
            // connection.setRequestProperty("Cookie","JSESSIONID=" + your_session_id);

            connection.setUseCaches(false);
            connection.connect();

            // Post data to remote server
            try (DataOutputStream wr = new DataOutputStream(connection.getOutputStream())) {
                wr.write(postData);

                // Read data response
                BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String content = "", line;
                while ((line = rd.readLine()) != null) {
                    content += line + "\n";
                }

                // Successful post and read
                params[0].resp_msg = content;
            } catch (Exception e) {
                // Error while reading content
                params[0].resp_msg = String.format(MOBILE_ERROR_RESPONSE, e.getMessage());
            }
        } catch (Exception e) {
            params[0].resp_msg = String.format(config.getServerUrl() + BAD_URL, url_str);
        }

        success = true;
        return true;
    }
}