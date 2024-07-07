from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

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