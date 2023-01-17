from pytube import YouTube
import subprocess
import os

AUDIO_ONLY = True

class YouTubeDownloader(YouTube):
    def __init__(self, category, name, title, link):
        YouTube.__init__(self,link)
        self.name = name # name of the artist
        self.title = title
        self.category = category
        self.link = link
        self.path = "/home/t/Videos/YouTube/" + self.category + "/"
        #self.path = os.path.join(self.category, self.name+"/"+self.title)

        self.tube_object = YouTube(self.link) # Create a youtube object       

        # Check if video is available
        assert self.tube_object.check_availability() == None, 'video does not seem to be available'

        if AUDIO_ONLY:
            self.tube_object_strm = self.tube_object.streams.get_audio_only()

        else:
            self.tube_object_strm = self.tube_object.streams.get_highest_resolution()        
    
        
        # default filename (youtube video title)
        self.default_filename = self.tube_object_strm.default_filename         
        
    def download(self):
        try:
            self.tube_object_strm.download(output_path=self.path, filename=self.name+"_"+self.title+".mp4")
        except Exception as e:
            print(e.message, e.args)

# main program

def main():
    category, artist, title = input("Enter the category (eg. mezmur, music, documentary), artist name, and title of song/video separated by a comma: ").split(", ")
    #category = input("Enter the category of the video: music, mezmur")
    #artist = input("Enter artist name: ")
    url = input("Enter link to the video: ")

    # Create an object of YoutubeDownloader
    ytd = YouTubeDownloader(name=artist, link=url, category=category, title=title)

    try:
        ytd.download()
    except:
        print("Something went wrong")

    if AUDIO_ONLY:
        # Convert mp4 file to mp3
        print("finalizing download. Converting mp4 to mp3 format.")
        new_file_name = ytd.name + ytd.title + ".mp3"
        # TODO: replace the terminal based ffmped conversion with AudioConvert python library  
        subprocess.run(['ffmpeg', '-i', os.path.join(ytd.path, ytd.name+"_"+ytd.title+".mp4"), 
        os.path.join(ytd.path, new_file_name)])
    


if __name__ == "__main__":
    try:
        main()

    except:
        print("Bad")


