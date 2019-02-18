from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import hashlib
# Create your views here.
def hello(request):
    return HttpResponse('hello!')

def index(request):
    return render(request,'index.html')

def upload(request):
    if request.method == 'POST':
        myfile = request.FILES.get('upfile')
        if  not myfile:
            return HttpResponse('没有上传文件!')
        file = myfile.read()
        if not file:
            return HttpResponse('不能上传空文件!')
        md5 = hashlib.md5(file).hexdigest()#取文件md5值
        filename = myfile.name
        filesize = myfile.size
        fileinfo = FileInfo.objects.filter()
        if fileinfo:
            FileInfo(name = filename,size = filesize,md5 = md5).save()
            return HttpResponse('文件已存在,秒传成功!')
        with open('file/{}'.format(md5),'wb') as fn:
            fn.write(file)
        #    FileInfo(name=filename, size=filesize, md5=md5).save()
        return HttpResponse('文件上传成功')
    else:
        return HttpResponse('get')

def content(request,md5):
    fileinfo = FileInfo.objects.filter(md5=md5)
    if not fileinfo:
        FileInfo(name=filename, size=filesize, md5=md5).save()
        return HttpResponse('该文件不存在或删除')
    context = {
        'name':FileInfo[0].name,
        'size':FileInfo[0].size,
        'url':'/file/{}'.format(fileinfo[0].name)
    }
    return render(request,'context.html',context=context)

def download(request):
    referer = request.META.get('HTP_REFERER')
    if not referer:
        return HttpResponse('该文件不存在或删除')
    mdt = referer[-33:-1]
    fileinfo = FileInfo.objects.filter(md5=md5)
    if not fileinfo:
        return HttpResponse('该文件不存在或删除')
    file = open('file/{}'.format(md5),'rb').read()
    response = HttpResponse(file)
    response['content-type']