from io import BytesIO
from pytube import YouTube

class Download():
    def __init__(self,url):

        self.url = url
        self.url_code = url.split("/")[-1]
        self.downloaded = None
        self.loaded = None
        self.yt_link = None
        self.buffer = None
        self.name = None


    def load(self):

        try:
            self.yt_link = YouTube(self.url)
            self.name = self.yt_link.title
            self.yt_link = self.yt_link.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            self.loaded = True

        except Exception as e:
            self.loaded = False
            
        return

    def download(self):

        for _ in range(512):
            try:
                self.buffer = BytesIO()
                self.yt_link.stream_to_buffer(self.buffer)
                self.buffer.seek(0)
                self.downloaded = True
                return

            except Exception as e:
                self.downloaded = False
                
        self.downloaded = False
        return

