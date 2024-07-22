from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
from .match import match_iris
import pathlib
from random import randint

def dec_rtrn(text):
    res=""
    m=n=0
    ln=len(text)
    k1=text[ln-1:ln-3:-1]
    k=k2=bits=""
    rl=0
    if k1[0]<k1[1]:
        rl=0
        lnt=ord(k1[1])-ord(k1[0])
        k=text[ln-1:ln-1-lnt:-1]
        m = ord(k[lnt-2]) - ord('m')
        n = ord(k[lnt-1]) - ord('n')
        k2=k[2:lnt-2]
    else:
        rl=1
        k1=k1[::-1]
        lnt=ord(k1[1])-ord(k1[0])
        k=text[ln-1:ln-1-lnt:-1]
        m = ord(k[lnt-1]) - ord('m')
        n = ord(k[lnt-2]) - ord('n')
        k2=k[2:lnt-2]
    
    for l in k2:
        dif=ord(l)-ord('A')
        tmp=""
        for i in range(5):
            tmp+=str(dif%2)
            dif=dif//2
        tmp=tmp[::-1]
        if rl==0:
            st=tmp[4]
            st+=tmp[0:4]
            tmp=st
        else:
            st=tmp[1:]
            st+=tmp[0]
            tmp=st
        bits=bits+tmp
        
    diff=ord(k1[0])-ord('a')
    bits=bits[ 0 : len(bits)-diff ]
    
    msg=""
    for i in range(len(bits)):
        if bits[i]=='0':
            msg += chr(ord(text[i])-m)
        else:
            msg += chr(ord(text[i])-n)
    res=msg
    return res

def match(request):
    if request.method == 'POST':
        file = request.FILES['imgfile']
        Org_data = file.read()
        file.close()
        dc=dec_rtrn(Org_data.decode())
        Byte_data=bytes.fromhex(dc)
        with open("static/output.jpg",'wb') as file: 
            file.write(Byte_data)
        result = match_iris("output.jpg")
        if result[1] > 40:
            return HttpResponse("Best Match: " + str(result[0]) +"\n"+ str(result[1]) +"  %")
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
        dc=dec_rtrn(Org_data.decode())
        Byte_data=bytes.fromhex(dc)
        with open("static/iris_data/"+name+".jpg",'wb') as file: 
            file.write(Byte_data)

        if pathlib.Path("static/iris_data/"+name+".jpg").is_file():
            return HttpResponse("Data Saved for "+ name +" Successfully")
        else:
            return HttpResponse("Error. Try Again.")
    return render(request,"base.html")