import os
import pandas as pd
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from Face_Recognition.face_rec import Face
from django.core.files.storage import FileSystemStorage


def gen(camera: Face):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               frame + b'\r\n\r\n'
               )

def index(request):
    return render(request, 'index.html')

def admin(request):
    if request.method == 'POST' and request.FILES['myFile']:
        myFile = request.FILES['myFile']
        fs = FileSystemStorage()
        fileName = request.POST['Role']+'-'+request.POST['Name']+'.jpg'
        fs.save(fileName, myFile)
    return render(request, 'admin.html')


def get_data(request):
    path = os.path.join(os.path.dirname(__file__),os.pardir)
    PROJECT_ROOT = os.path.abspath(path)
    data = pd.read_csv(os.path.join(PROJECT_ROOT, 'Data.csv'))
    data = data.sort_values(by=["Time"], ascending=False)
    data = data.head()
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, "table.html", context)


def webcam_feed(request):
    return StreamingHttpResponse(gen(Face()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')