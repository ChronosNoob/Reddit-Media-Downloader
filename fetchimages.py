import json
import praw
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from io import BytesIO
import requests
import time
import datetime
import os
from redvid import Downloader


def add_margin(pil_img, bottom):
    width, height = pil_img.size
    new_height = height + bottom
    result = Image.new(pil_img.mode, (width, int(new_height)), (50,50,50))
    result.paste(pil_img, (0, 0))
    return result


def GetPosts(Subreddits,TopPosts):
	CompleteData = []
	SubredditData = []
	with open("UserData.json", "r") as read_file:
    		data = json.load(read_file)
	reddit = praw.Reddit(
						client_id = data["client_id"] ,
						client_secret = data["client_secret"] ,
						username = data["username"] ,
						password = data["password"] , 
						user_agent = data["user_agent"]
						)
	for i in range(len(Subreddits)):
		print(Subreddits[i])   
		try:
			subreddit = reddit.subreddit(Subreddits[i])
			for submission in subreddit.hot(limit=TopPosts):
				print("Post Titled: " + submission.title)
				imgurls = []
				if "gallery" in submission.url:
					for i in submission.media_metadata.items():
						URL = i[1]['p'][0]['u']
						URL = URL.split("?")[0].replace("preview", "i")
						imgurls.append(URL)
				else:
					imgurls.append(submission.url)
				print("\n")
				SubmissionData = [submission.title,imgurls]
				SubredditData.append(SubmissionData)
			CompleteData.append(SubredditData)
			CompleteData.append(subreddit.url)
		except:
			print("Error: Does the subreddit exist?")
	return CompleteData

def Export(CompleteData,quality):
	now = datetime.datetime.now()
	dtstring = now.strftime("%b-%d-%Y %H:%M:%S")
	for subredditindex in range(0,len(CompleteData),2):
		subredditname = CompleteData[subredditindex+1]
		subreddit = CompleteData[subredditindex]
		subredditname = subredditname.strip("r/")
		directory = dtstring + "/" + subredditname
		if not os.path.exists("exported/"+directory):
			os.makedirs("exported/"+directory)
		for submission in subreddit:
			#print(submission)
			Title = submission[0]
			urls = submission[1]
			if "v.redd.it" in urls[0]:
				downloader = Downloader(max_q=True)
				downloader.url = urls[0]
				downloader.filename = "exported/"+directory+"/"+Title
				downloader.download()
				continue
			try:
				for imgurl in urls:
					response = requests.get(imgurl)
					print(imgurl)
					if response.status_code == 200:
						image_data = BytesIO(response.content)
						im = Image.open(image_data)
					print("Image opened")
					width, height = im.size
					TitleFontSize = 1
					Font = ImageFont.truetype("afont.ttf", TitleFontSize)
					img_fraction = 0.8
					#print(Font.getlength)
					#print(img_fraction*width)
					while Font.getlength(Title) < img_fraction*width:
						# iterate until the text size is just larger than the criteria
						# print(Font.getlength)
						TitleFontSize += 1
						Font = ImageFont.truetype("afont.ttf", TitleFontSize)
						left,top,right,bottom = Font.getbbox(Title)
						Fontheight = bottom - top
					margin = Fontheight*1.5
					pad = (0.10 * margin) + height
					margin += 0.10*margin
					paddedimage = add_margin(im,margin)
					Draw = ImageDraw.Draw(paddedimage)	
					Draw.text((im.size[0]*0.01,pad),Title,(255,255,255), font=Font)
					print("Image pasted")
					paddedimage.save("exported/"+directory+"/"+Title+".jpg", quality=quality,optimize=True)
					paddedimage.close()
			except:
				print("FAIL")



PostCount = input("How many top posts should be exported?: ")
Subreddits = str(input("Enter subreddits of choice (Separated by commas) : "))
qualitychoice = int(input("What quality do you want the file to be compressed to? \nOn a scale of 1-100. 90+ reccomended for optimum quality \nVideos will be automatically downloaded at max resolution \n-------: "))
SplitReddits = Subreddits.split(",")
FuncSubreddits = SplitReddits
CompleteData = GetPosts(FuncSubreddits,int(PostCount))
Export(CompleteData,qualitychoice)