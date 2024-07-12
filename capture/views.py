from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
from .match import knn_match

def home(request):
    if request.method == 'POST':
        file = request.FILES['imgfile']
        fs = FileSystemStorage(location="static/") #defaults to   MEDIA_ROOT  
        fs.delete("output.jpg")
        filename = fs.save("output.jpg", file)
        file_url = fs.url(filename)
        return render(request, 'base.html', {
            'file_url': file_url
        })
    return render(request,"base.html")

def match(request):
    if request.method == 'POST':
        file = request.FILES['imgfile']
        fs = FileSystemStorage(location="static/") #defaults to   MEDIA_ROOT  
        fs.delete("output.jpg")
        fs.save("output.jpg", file)
    result = knn_match("output.jpg")
    return HttpResponse(str(result[0]) + '<br>'+ str(result[1]))
    # return render(request,"base.html")