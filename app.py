from flask import Flask, render_template, redirect, request, url_for,send_file
from downloader import Download as YouTube

app = Flask(__name__)
link = Youtube(__name__)

@app.route("/")
def home():
    global link
    link = YouTube(__name__)
    return render_template("homepage.html")




@app.route("/loader",methods = ["GET","POST"])
def loader():
    global link

    if request.method == "POST":
        url = request.form["url"]
        link = YouTube(url)
        
        link.load()

        return "Loaded"

    return redirect(url_for("home"))




@app.route("/download", methods = ["GET"])
def downloadPage():
    global link

    if link.loaded == True:
        return render_template("downloadpage.html",code = link.url_code)

    elif link.loaded == False:
        return render_template("error.html",error = "Link Not Found",description = "Enter a valid link or check your Internet Connection")

    elif link.loaded == None:
        return redirect(url_for("home"))




@app.route("/downloadfunction",methods = ["GET","POST"])
def downloader():
    global link
    
    if request.method == "POST":
        link.download()

        return "Downloaded"

    return redirect(url_for("home"))



@app.route("/downloaded",methods = ["GET"])
def sender():
    global link

    if link.downloaded == True:
    
        buffer,name = link.buffer,link.name
        link = YouTube(__name__)

        return send_file(buffer,as_attachment=True,download_name=f"{name}.mp4",mimetype="video/mp4")


    elif link.downloaded == False:
        return render_template("error.html",error = "Download Failed",description = "Something Unexpected happened! Try again.")

    elif link.downloaded == None:
        return redirect(url_for("home"))




@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error = "Error - 404",description = "Page Not Found")



if __name__ == "__main__":
    app.run()
