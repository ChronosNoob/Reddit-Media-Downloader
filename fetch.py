
import json
import praw
from colorama import Fore,Back,Style
def GetPosts(Subreddits,TopPosts):
    CompleteData = []
    SubredditData = []
    with open("UserData.json", "r") as read_file: # Reads login details.json
            data = json.load(read_file) #Converts json to dict
    reddit = praw.Reddit(
                        client_id = data["client_id"] ,
                        client_secret = data["client_secret"] ,
                        username = data["username"] ,
                        password = data["password"] , 
                        user_agent = data["user_agent"]
                        )
    for i in range(len(Subreddits)):
        print(Fore.CYAN + Subreddits[i] + Style.RESET_ALL) #Prints subreddit name  
        try:
            subreddit = reddit.subreddit(Subreddits[i]) #Instantiates subreddit 
            SubredditData = [] #Initialises empty data list
            for submission in subreddit.hot(limit=TopPosts):
                try:
                    #print("Post Titled: " + submission.title)
                    imgurls = [] # makes empty url list
                    if "gallery" in submission.url: #if post is a gallery find the image urls
                        for i in submission.media_metadata.items():
                            URL = i[1]['p'][0]['u']
                            URL = URL.split("?")[0].replace("preview", "i")
                            imgurls.append(URL)
                    else:
                        imgurls.append(submission.url) # adds post url if not a gallery
                    #print("\n")
                    SubmissionData = [submission.title,imgurls] 
                    NewData = [SubmissionData,submission.url] #Redundant
                    SubredditData.append(NewData)
                except Exception as e:
                    print("Post Error: " + str(e) + "\n" + str(submission.url) + "\nMost likely not an image/gallery")
            #print(subreddit.url)
            SubredditData = [SubredditData,subreddit.url] 
            #print(NewData)
            CompleteData.append(SubredditData)
        except Exception as error:
            print("Error: Does the subreddit exist?:  \n" + str(error)) # Error handling
    return CompleteData
