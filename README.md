# Mycroft AI Ping Skill

This is a 3rd party skill that uses keywords to get either a server's ping time or status. This can be used to check that a server is responding correctly. Alternatively, one can use this to send GET requests to a server to start or stop services. By using the Ping Skill, custom commands can be created for unique online services.

For instance, saying, `Mycroft: Ping Google` garners a reply of `Pinged in 9.03 milliseconds.`

If a keyword is set to get the server response, then Mycroft will reply, `Server says: OK 200`, or `Response is: Bad Gateway 502`, et cetera.

---

Configuration is stored in a text file, `hosts.txt`, with one server per line:

    google,0,https://google.com
    
This line will tell the Ping Skill that `google` is the keyword, 0 is for a ping response and then the URL to ping. Alternatively, this

    linux,1,https://linux.com
    
will respond with the server status of linux.com, because of the `1` after the keyword.

If you are running a server that can respond to GET requests, such as using [Huginn](https://github.com/cantino/huginn) (or other IFTT software), then a setting like

    hug, 1, http://www.yourdomain.com/users/1/web_requests/2/supersecretstring

and the corresponding Huginn Web Hook Agent on the remote end will suffice to have a Mycroft remote control for the server. Saying `Mycroft: Ping Hug` will load that URL, which will execute code on the server. Mycroft will receive the custom server response, `Event Created 201`.

