from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import JobsForm
import json


# imports for pdf automating starts
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import zipfile


# imports for converting file to image start
import tempfile
import pdf2image
from PIL import Image
from PyPDF2 import PdfFileReader


def automate_and_create_zip(request):
    names = request.FILES['invitees'].file
    invite = request.FILES['invite'].file
    x_coords = float(request.POST['x-coords'])
    y_coords = float(request.POST['y-coords'])

    # os.makedirs("auto_pdf_dir") #directory where the files will be stored
    for line in names:
        invitee = line.strip()
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(x_coords, y_coords, invitee)
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(invite)
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = open("auto_pdf_dir/"+str(invitee)+".pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        print("done")

    # when done, create a zip file of the folder

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    # converting to zip for downloading
    zipf = zipfile.ZipFile('auto_pdf_dir.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir("auto_pdf_dir", zipf)

    return HttpResponse(json.dumps({"status": 'OK'}))


# DECLARE CONSTANTS
DPI = 200
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False


def pdftopil(pdf_path):
    pil_images = pdf2image.convert_from_path(pdf_path, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE,
                                             last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD,
                                             use_cropbox=USE_CROPBOX, strict=STRICT)
    return pil_images


def save_images(pil_images, file):
    # save each pil_image in the static file
    # TODO: explore working with temp dir to display image
    for image in pil_images:
        image.save(file)


def convert_pdf_to_image(path):
    output_file = "static/automate_pdf/imgs/__invite.jpg"  # TODO: Make use of python tempfile function
    pil_images = pdftopil(path)
    save_images(pil_images, output_file)

    return output_file


def index(request):
    if request.method == "POST":
        job_form = JobsForm(request.POST, request.FILES)
        if job_form.is_valid():
            print("job form is valid")
            job = job_form.save()

            automate_and_create_zip()  # function to create pdfs for all invitees
            file_url = ""
            return render(request, 'automate_pdf/pages/download.html', {"file": file_url})
        else:
            print("form not valid")
            print(job_form.errors)
            return HttpResponse("Form not valid")

    else:
        print("get")
        form = JobsForm()
        return render(request, 'automate_pdf/pages/index.html', {"form": form})


def download_file(request):
    if request.method == "GET":
        zip_file = open('/Users/nelson/Documents/Projects/auto_pdf/auto_pdf_dir.zip', 'rb')
        return FileResponse(zip_file)


def get_position(request):
    _, file = tempfile.mkstemp(suffix='.pdf')
    fp = open(file, 'wb')
    pdf_file = request.FILES['file'].file
    if request.method == "POST":
        try:
            for line in pdf_file:
                fp.write(line)

            image_url = convert_pdf_to_image(file)
            pdf = PdfFileReader(pdf_file).getPage(0).mediaBox
            response = {"src": image_url, "width": str(pdf.getWidth()),
                        "height": str(pdf.getHeight()), "status": 'OK'}
        except Exception as e:
            print(e)
            response = {"status": 'NOK', "error": "An Error occured when converting the pdf"}

        return HttpResponse(json.dumps(response))

