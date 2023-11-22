
import json
import praw
from colorama import Fore,Back,Style

def FetchPostData(submission):
    try:
        #print("Post Titled: " + submission.title)
        imgurls = [] # makes empty url list
        if "gallery" in submission.url: #if post is a gallery find the image urls
            for i in submission.media_metadata.items():
                URL = i[1]['p'][0]['u']
                URL = URL.split("?")[0].replace("preview", "i")
                imgurls.append(URL)
                #print(URL)
        else:
            imgurls.append(submission.url) # adds post url if not a gallery
        #print("\n")
        SubmissionData = [submission.title,imgurls] 
        #print(SubmissionData)
        return SubmissionData
    except:
        print("Submission Error")
def FetchSectors(TopPosts,subreddit,top,toptype):
    subredditdata = []
    if int(TopPosts) > 1000:
                for i in range((TopPosts // 1000 ) + 1):
                    if i == (TopPosts // 1000) + 1:
                        for submission in FetchWhich(limit = TopPosts % 1000,subreddit=subreddit,top=top,toptype=toptype):
                            subredditdata.append(FetchPostData(submission))
                    else:
                        for submission in FetchWhich(limit = 1000,subreddit=subreddit,top=top,toptype=toptype):
                            subredditdata.append(FetchPostData(submission))
    else:
        for submission in FetchWhich(limit = TopPosts,subreddit=subreddit,top=top,toptype=toptype):
            subredditdata.append(FetchPostData(submission))
    #print(subredditdata)
    return subredditdata

def FetchWhich(limit,subreddit,top,toptype):
    #print(top)
    #print(toptype)
    if top == True:
        posts = subreddit.top(limit=limit,time_filter=toptype)
    else:
        posts = subreddit.hot(limit=limit)
    return posts

def GetSubredditPosts(Subreddits,TopPosts,top,toptype):
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
            SubredditData = FetchSectors(TopPosts,subreddit,top,toptype)
            #print(subreddit.url)
            SubredditData = [SubredditData,subreddit.url] 
            #print(NewData)
            CompleteData.append(SubredditData)
            #print(len(SubredditData[0]))
        except Exception as error:
            print("Error: Does the subreddit exist?:  \n" + str(error)) # Error handling
    return CompleteData
