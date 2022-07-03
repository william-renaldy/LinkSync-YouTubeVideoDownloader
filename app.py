from io import BytesIO
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from pytube import YouTube


app = Flask(__name__)
loaded = None
download_successful = None


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/download", methods = ["GET","POST"])
def download():
    if request.method == "POST":
        global link,code,loaded

        url = request.form["url"]
        code = url.split("/")[-1]

        try:
            link = YouTube(url)
            link = link.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            loaded = True
            return render_template("downloadpage.html",code = code)
            
        except Exception as e:
            loaded = False
            print(e)
            return render_template("error.html",error = "Link Not Found",description = "Enter a valid link or check your Internet Connection")

    return redirect(url_for("home"))



@app.route("/downloader",methods = ["GET"])
def downloader():
    global loaded
    if loaded == True:
        try:
            global code

            return render_template("downloadpage.html",code=code)
        except Exception as e:
            print(e)
            return redirect(url_for("home"))

    if loaded == None:
        return redirect(url_for("home"))

    if loaded == False:
        return render_template("error.html",error = "Link Not Found",description = "Enter a valid link or check your Internet Connection")
    




@app.route("/downloaded",methods = ["GET"])
def downloaded():
    if download_successful == True:
        try:
            global buffer,link
            return send_file(buffer,as_attachment=True,download_name=f"{link.title}.mp4",mimetype="video/mp4")
        except Exception as e:
            print(e)
            return render_template("error.html",error = "Download Failed",description = "Something Unexpected happened! Try again.")

    elif download_successful == False:
        return render_template("error.html",error = "Download Failed",description = "Something Unexpected happened! Try again.")

    elif download_successful == None:
        return redirect(url_for("home"))



@app.route("/downloadfunction",methods = ["GET","POST"])
def DownloadPage():
    if request.method == "POST":
        global link,buffer,download_successful

        for _ in range(100):
            try:
                buffer = BytesIO()
                print(link)
                link.stream_to_buffer(buffer)
                buffer.seek(0)
                download_successful = True
                return "Success"

            except Exception as e:
                download_successful = False
                print(e)
                continue
        return render_template("error.html",error = "Download Failed",description = "Something Unexpected happened! Try again.")

    return redirect(url_for("home"))




@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error = "Error - 404",description = "Page Not Found")


if __name__ == "__main__":
    app.run(debug=True)
