
import threading
import export as ExportActions
import fetch as WebActions
PostCount = input("How many hot posts should be exported? (Be aware there may be more files than this created due to galleries): ") #Takes in number of posts to be exported
while True:
    if PostCount.isnumeric() == False:
        PostCount = input("Invalid input: How many hot posts should be exported?: ") # Asks the user to input number again if input is not numeric
    else:
        break
Subreddits = str(input("Enter subreddits of choice (Separated by commas) : ")).strip(" ") # Takes in subreddits input and removes spaces
while True:
    if Subreddits == None or Subreddits == "":
        Subreddits = str(input("Invalid input: Enter subreddits of choice (Separated by commas) : ")).strip(" ")
    else:
        break
qualitychoice = input("What quality do you want the file to be compressed to? \nOn a scale of 1-100. 90+ reccomended for optimum quality \nVideos will be automatically downloaded at max resolution \n-------: ") #Takes user data for desired quality
while True:
    if int(qualitychoice) == None or int(qualitychoice) > 100 or int(qualitychoice) < 0 or qualitychoice.isnumeric() == False:
        qualitychoice = int(input("Invalid Input: What quality do you want the file to be compressed to? \nOn a scale of 1-100. 90+ recommended for optimum quality \nVideos will be automatically downloaded at max resolution \n-------: ")) #Takes user data for desired quality
    else:
        break
TitleOnImage = input("Do you want the title to be visible on the image? (Y/N) \nInput Here: ")
if TitleOnImage == "Y" or TitleOnImage == "y":
    TitleOnImage = True
else:
    TitleOnImage = False
MaxHeight = input("Enter maximum height in pixels (3000 recommended) : ") # Takes maximum width
while True:
    if PostCount.isnumeric() == False:
        PostCount = input("Invalid input: Enter maximum height: ") # Asks the user to input number again if input is not numeric
    else:
        break
MaxWidth = input("Enter maximum width for resizing (2000 recommended) : ") #Takes in number of posts to be exported
while True:
    if PostCount.isnumeric() == False:
        PostCount = input("Invalid input: Enter maximum width in pixels (2000 recommended): ") # Asks the user to input number again if input is not numeric
    else:
        break

top = input("Do you want to download 'top' or 'hot' posts? : ")
while True:
    if top == "Top" or top == "top" or top == True:
        top = True
        toptype = input("Enter time filter in lowercase(e.g 'all'): ")
        if toptype in ("all", "hour", "month", 'week', 'day', "year"):
            break
    if top == "hot" or top == 'Hot':
        top = False
        break
    else:
        top = input("Invalid Input: Do you want to download 'top' or 'hot' posts? : ")
SplitReddits = Subreddits.split(",")#Splits input into array
CompleteData = WebActions.GetSubredditPosts(SplitReddits,int(PostCount),top,toptype)

if len(CompleteData) != 1: #Threads code with two threads if there is more than one subreddit
    midpoint = len(CompleteData) // 2
    first_half = CompleteData[:midpoint]
    second_half = CompleteData[midpoint:]
    ThreadOne = threading.Thread(target=ExportActions.Export,args=(first_half,qualitychoice,TitleOnImage,MaxWidth,MaxHeight,1)) 
    ThreadTwo = threading.Thread(target=ExportActions.Export,args=(second_half,qualitychoice,TitleOnImage,MaxWidth,MaxHeight,2))
    ThreadOne.start()
    ThreadTwo.start()
    ThreadOne.join()
    ThreadTwo.join()
else:
    ExportActions.Export(CompleteData,qualitychoice,TitleOnImage,MaxWidth,MaxHeight, 1)
