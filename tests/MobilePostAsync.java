// import android.content.CursorLoader;
// import android.content.Loader;
// import android.database.Cursor;
// import android.net.Uri;
// import android.os.AsyncTask;
// 
// import android.os.Build;
// import android.os.Bundle;
// import android.provider.ContactsContract;
// import android.text.TextUtils;
// import android.view.KeyEvent;
// import android.view.View;
// import android.view.View.OnClickListener;
// import android.view.inputmethod.EditorInfo;
// import android.widget.ArrayAdapter;
// import android.widget.AutoCompleteTextView;
// import android.widget.Button;
// import android.widget.EditText;
// import android.widget.TextView;
// import android.util.Log;
import server_config.ServerConfig;
import post_data.PostData;

import java.lang.Integer;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import javax.net.ssl.HttpsURLConnection;


public class MobilePost extends AnsyncTask<Void, Void, Boolean> {

  // Pull server configuration information
  final static ServerConfig config = new ServerConfig();

  // POST method input
  private String postString;
  private String urlString;
  private int content_type_in;

  // Supported content types to post data
  public enum ContentType {
    JSON, TXT, CSV
  }

  // Return network error message
  final String MOBILE_ERROR_RESPONSE = "{\"error\": \"%s\"}";

  // Exception messages
  final String BAD_URL = "Malformed URL: %s";
  final String BAD_CONTENT_TYPE = "Unsupported content type: %d";

  // Sends HTTP POST request with postString as data to server/url_str with
  // content type content_type_in
  @Overide
  protected String doInBackground(PostMessage... params) {
      // Pull POST properties from passed param
      String postString = params[0].postString;
      String content_type_in = params[0].contentType;
      String url_str = params[0].UrlString;

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
        URL url = new URL(config.SERVER_URL + url_str);

        // Start HTTP POST connection
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setConnectTimeout(5000);
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
            return content;
        } catch (Exception e) {
            // Error while reading content
            return String.format(MOBILE_ERROR_RESPONSE, e.getMessage());
        }
      } catch (Exception e) {
        throw new java.lang.Error(String.format(config.SERVER_URL + BAD_URL, url_str));
      }
  }

  public static void main(String args[]) {
    if (args.length != 2) {
      System.out.println("Content type and test string required as input");
      System.out.println("  Content Types:");
      for (ContentType value: ContentType.values()){
        value.ordinal();
        System.out.format("    %-6s: %d\n", value.name(), value.ordinal());
      }
      System.exit(-1);
    }

    // Test mobile echo response
    MobilePost echoRequest = new MobilePost();
    String response;
    int content_type = Integer.parseInt(args[0]);

    response = echoRequest.doInBackground(args[1], "mobile/echo/", content_type);
    System.out.println("---------- Server Response ----------");
    System.out.println(response);
    System.out.println("-------------------------------------");
  }

}
