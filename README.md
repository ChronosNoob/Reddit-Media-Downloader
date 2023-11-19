# Reddit-Media-Downloader

This is a python script that will download videos or images from reddit. If the downloaded media is an image it will add the title of the post to the bottom of the screen. Uses 2 thread multithreading and thus needs at least two threads (all modern CPU's are capable of this)
Authorisation data should be placed in UserData.json in this format.

![image](https://github.com/ChronosNoob/Reddit-Media-Downloader/assets/83444922/184d7d8e-673c-4799-9da0-ee50c5e0526a)

GUI may be added in the future but is not a priority.

**Installation:**

Open cmd/terminal to repository location and run `pip install -r requirements.txt`

**Setup:**

Go to https://www.reddit.com/prefs/apps

Create new script with desired name and description, set redirect url to **the full version** of any websites url.

![image](https://github.com/ChronosNoob/Reddit-Media-Downloader/assets/83444922/2f05add9-e194-4f44-a915-7f4f2202fdae)

Enter the secret and id from the application you just made into **UserData.json**

![image](https://github.com/ChronosNoob/Reddit-Media-Downloader/assets/83444922/89d93829-e66d-4dea-a007-f1bb0a1afda0)

Add your username and password to **UserData.json**

**Usage**

Run main.py
