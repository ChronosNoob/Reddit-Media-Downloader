# Reddit-Media-Downloader

This is a python script that will download videos or images from reddit. If the downloaded media is an image it will add the title of the post to the bottom of the screen. Uses 2 thread multithreading and thus needs at least two threads (most modern cpus have this anyways)
Authorisation data should be placed in UserData.json in this format.


{
    "client_id" : "client id here",
    "client_secret" : "client secret here",
    "username" : "username here",
    "password" : "password here",
    "user_agent" : "Python Reddit Post Exporter"
}
