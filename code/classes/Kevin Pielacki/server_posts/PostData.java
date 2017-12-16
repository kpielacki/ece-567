package com.example.xingxiang25.userprofile.server_posts;

/**
 * Created by xingxiang25 on 12/8/2017.
 */
public class PostData {

    private String url_string;
    private String post_string;
    private int content_type;
    public String resp_msg;

    public PostData(String urlString, String postString, int contentType) {
        url_string = urlString;
        post_string = postString;
        content_type = contentType;
        resp_msg = "";
    }

    public String getUrlString() {
        return url_string;
    }

    public String getPostString() {
        return post_string;
    }

    public int getContentType() {
        return content_type;
    }
}