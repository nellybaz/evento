from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import JobsForm


###### imports for pdf automating starts ##############
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import zipfile
###### imports for pdf automating ends ##############


#### imports for converting file to image start #####
import pdf2image
from PIL import Image
#### imports for converting file to image end #####
 
def automate_and_create_zip():
    names = open("invitees/names", "r")

    os.makedirs("auto_pdf_dir") #directory where the files will be stored
    for line in names:
        invitee = line.strip()
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(50, 420, invitee)
        can.save()

        #move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("invite_files/invite.pdf", "rb"))
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

    #when done, create a zip file of the folder

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))



    #converting to zip for downloading
    zipf = zipfile.ZipFile('auto_pdf_dir.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir("auto_pdf_dir", zipf)


    #convert pdf to image



#DECLARE CONSTANTS
PDF_PATH = "/Users/nelson/Documents/Projects/auto_pdf/invite_files/invite.pdf"
DPI = 200
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False

def pdftopil():
    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    return pil_images
    
def save_images(pil_images):
    #This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    for image in pil_images:
        image.save("__invite" + str(index) + ".jpg")
        index += 1




def convert_pdf_to_image(request):
    if request.method == "GET":
        pil_images = pdftopil()
        save_images(pil_images)
        # # pdf = wi(filename='/Users/nelson/Documents/Projects/auto_pdf/invite_files/invite.pdf', resolution=300)
        # # pdfImage = pdf.convert("jpeg")

        # # for img in pdfImage.sequence:
        # #     converted_image = wi(image=img)
        # #     converted_image.save(filename="__inviteImage.jpg")

        return HttpResponse("image generated")




def index(request):
    if request.method == "POST":
        job_form = JobsForm(request.POST, request.FILES)
        if job_form.is_valid():
            print("job form is valid")
            job = job_form.save()

            automate_and_create_zip() #function to create pdfs for all invitees 
            file_url = ""
            return render(request, 'automate_pdf/pages/download.html', {"file": file_url})
        else:
            print("form not valid")
            print(job_form.errors)
            return HttpResponse("Form not valid")

    else:
        print("get")
        form  = JobsForm()
        return render(request, 'automate_pdf/pages/index.html', {"form": form})


def download_file(request):
    if request.method == "GET":
        zip_file = open('/Users/nelson/Documents/Projects/auto_pdf/auto_pdf_dir.zip', 'rb')
        return FileResponse(zip_file)

def get_position(request):
    if request.method == "GET":
        image_url = ""
        return render(request, 'automate_pdf/pages/get_position.html', {"image": image_url})