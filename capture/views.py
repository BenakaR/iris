from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
from .match import match_iris
import pathlib
from random import randint
from cryptography.fernet import Fernet

#key = Fernet.generate_key()
key = b'bY7JXmRqIyzj4kdkc_YBwJwzTOlc2WEfflGx8RauxaQ='

fnet = Fernet(key)


def match(request):
    if request.method == 'POST':
        file = request.FILES['imgfile']
        Org_data = file.read()
        file.close()
        decrypted_data = fnet.decrypt(Org_data)
        with open("static/output.jpg", "wb") as file:
            file.write(decrypted_data)
        result = match_iris("output.jpg")
        if result[1] > 40:
            return HttpResponse("Best Match: " + str(result[0]) +"\n"+ str(round(result[1],4)) +"  %")
        else:
            return HttpResponse("Not Matched")
    return render(request,"base.html")

def home(request):
    # if request.method == 'POST':
    #     file = request.FILES['imgfile']
    #     fs = FileSystemStorage(location="static/") # defaults to MEDIA_ROOT  
    #     fs.delete("output.jpg")
    #     fs.save("output.jpg", file)
    result = match_iris("output.jpg")
    return HttpResponse(str(result[0]) + str(result[1]))
    # return render(request,"base.html")

def new(request):
    if request.method == 'POST':
        file = request.FILES['imgfile']
        name = request.POST['name']
        if pathlib.Path("static/iris_data/"+name+".jpg").is_file():
            return HttpResponse("Data already exists")
        Org_data = file.read()
        decrypted_data = fnet.decrypt(Org_data)
        with open("static/iris_data/"+name+".jpg", "wb") as file:
            file.write(decrypted_data)
        if pathlib.Path("static/iris_data/"+name+".jpg").is_file():
            return HttpResponse("Data Saved for "+ name +" Successfully")
        else:
            return HttpResponse("Error. Try Again.")
    return render(request,"base.html")