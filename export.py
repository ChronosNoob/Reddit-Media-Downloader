
import datetime
import time
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests
from redvid import Downloader
from pytube import YouTube
from io import BytesIO
from colorama import Fore,Back,Style

def downloadyoutubevideo(link,directory):
    youtubeobject = YouTube(link)
    youtubeobject = youtubeobject.streams.get_highest_resolution()
    try:
        youtubeobject.download('exported/'+directory)
        print("Downloaded")
    except:
        print("Youtube fetching error has occured")

def add_margin(pil_img, bottom): #Adds space for title on the bottom of images
    width, height = pil_img.size
    new_height = height + bottom
    result = Image.new(pil_img.mode, (width, int(new_height)), (50,50,50)) #New image with extra space
    result.paste(pil_img, (0, 0))
    return result

def Export(CompleteData,quality,TitleOnImage,MaxWidth,MaxHeight):
    now = datetime.datetime.now() #Gets current date and time
    #print(CompleteData)
    dtstring = now.strftime("%b-%d-%Y %H:%M:%S") #Turns date and time to formatted string
    for subredditindex in range(len(CompleteData)):
        subredditname = CompleteData[subredditindex][1] #grabs subreddit name in r/ form
        subreddit = CompleteData[subredditindex][0] # grabs subreddit data
        #print(subredditname)
        subredditname = subredditname.strip("r/") #removes r/ from name as it will create a new directory
        directory = dtstring + "/" + subredditname # sets output directory
        #print(directory)
        #print(subreddit)
        time.sleep(10)
        if not os.path.exists("exported/"+directory): #makes directory if it does not exist already, exists for possibility of two instances running simultaneously
            os.makedirs("exported/"+directory)
        for submission in subreddit: #iterates through subreddit data
            #print(submission) #Debug
            Title = submission[0][0] #Grabs Title
            urls = submission[0][1] #Grabs URLs
            #print(urls) #Debug
            if "v.redd.it" in urls[0]: #Checks if url is reddit video url
                downloader = Downloader(max_q=True) 
                downloader.url = urls[0]
                downloader.filename = "exported/"+directory+"/"+Title
                downloader.download() # Downloads video
                continue
            elif "youtube" in urls[0] or "youtu.be" in urls[0]: #Checks if url is youtube link
                print("Attempting to download youtube video.")
                downloadyoutubevideo(urls[0],directory)
                continue
            elif "imgur" in urls[0]: # Checks if url is imgur link, will be downloaded in future
                continue
            elif "redgif" in urls[0]:
                continue
            elif "gif" in urls[0]:
                continue
            count = 0 #numbering for galleries
            for imgurl in urls: #loops through urls
                start_time = time.time()
                try:
                    count += 1
                    response = requests.get(imgurl) #gets raw image from internet
                    #print("ImageURL: " + imgurl)
                    if response.status_code == 200:
                        image_data = BytesIO(response.content) #turns image into file
                        im = Image.open(image_data)
                    #print("Image opened")
                    if TitleOnImage is True:
                        TitleDraw = subredditname +" - "+ Title
                        width, height = im.size #grabs height
                        TitleFontSize = 1
                        Font = ImageFont.truetype("afont.ttf", TitleFontSize)
                        img_fraction = 0.8
                        #print(Font.getlength) #Debug
                        #print(img_fraction*width) #Debug
                        while Font.getlength(TitleDraw) < img_fraction*width and TitleFontSize < 200:
                            # iterate until the text size is just larger than the criteria
                            # print(Font.getlength) #Debug
                            TitleFontSize += 1
                            Font = ImageFont.truetype("afont.ttf", TitleFontSize)
                            left,top,right,bottom = Font.getbbox(TitleDraw) # Gets the coords of each corner of the text. In use instead of .getsize() as getsize is deprecated
                            Fontheight = bottom - top #finds height from coords
                        margin = Fontheight*1.5 # Finds margin height based on size of font
                        pad = (0.10 * margin) + height # Gives location for text to be written based on margin height
                        margin += 0.10*margin # adds padding height to margin size on the bottom to have quasi-equal spacing
                        paddedimage = add_margin(im,margin) # Refer to function
                        Draw = ImageDraw.Draw(paddedimage)    
                        Draw.text((im.size[0]*0.01,pad),TitleDraw ,(255,255,255), font=Font) # Writes text to image
                        #print("Image pasted")
                    else:
                        paddedimage = im
                    #paddedimage = paddedimage.convert('RGB') #Forces image to RGB if it has transparency data
                    filetype = im.format
                    if filetype == "GIF":
                        paddedimage.close()
                        continue
                    paddedimage.thumbnail((int(MaxWidth),int(MaxHeight)))
                    paddedimage.save("exported/"+directory+"/"+Title + str(count)+"."+filetype, quality=quality,optimize=True)
                    paddedimage.close()
                    finaltime = (time.time() - start_time)
                    print(Fore.GREEN+str(count) + ": Media: "+Title + "  " + imgurl + " took " + str(finaltime)+Style.RESET_ALL  )
                except Exception as error:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print("Error: ",exc_type, fname, exc_tb.tb_lineno)
                    finaltime = (time.time() - start_time)
                    print("Failed MediaURL : " + imgurl + " took " + str(finaltime) + " to fail" )
