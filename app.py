from io import BytesIO
from flask import Flask, redirect, render_template, send_file, url_for, request, session
from pytube import YouTube
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/loader",methods = ["POST","GET"])
def loader():
    global url

    if request.method == "POST":
        url = request.form["url"]
        
        try:
            YouTube(url)
        except:
            return render_template("error.html",error = "Link Not Found",description = "Enter a valid link or check your Internet Connection")

        session[url] = url

        return "loaded"

    if request.method == "GET":
        return redirect(url_for("home"))




@app.route("/download",methods = ["GET"])
def downloadPage():


    try:
        print(url)
        print(session)

        if url in session:
            link = session[url]
            return render_template("downloadpage.html",code = link.split("/")[-1])

        else:
            return redirect(url_for("home"))

    except NameError:
        return redirect(url_for("home"))





@app.route("/downloadfunction",methods = ["GET","POST"])
def downloader():
    global buffer
    
    if request.method == "POST":
        
        if url in session:
            link = session[url]

            for _ in range(512):
                try:
                    link = YouTube(link).streams.filter(progressive=True,file_extension="mp4").get_highest_resolution()
                    buffer = BytesIO()

                    link.stream_to_buffer(buffer)
                    buffer.seek(0)
                    break
                
                except:
                    continue

            else:
                return render_template("error.html",error = "Download Failed",description = "Something Unexpected happened! Try again.")

            return "Downloaded"

        else:
            return redirect(url_for("home"))

    else:
        return redirect(url_for("home"))




@app.route("/downloaded",methods = ["GET"])
def sender():


    try:
        if url in session:

            link = session[url]
            name = YouTube(link)

            session.pop(url,None)

            return send_file(buffer,as_attachment=True,download_name=f"{name.title}.mp4",mimetype="video/mp4")

        else:
            return redirect(url_for("home"))

    except NameError:
        return redirect(url_for("home"))





if __name__ == "__main__":
    app.run(debug=True)
