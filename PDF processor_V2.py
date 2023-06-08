import base64
import csv
from csv import DictWriter
import os
from os import path
from PyPDF2 import PdfWriter, PdfReader #make sure to install the library using "pip3 install PyPDF2" 

def ProcessPDF(WDir,FName):  

    Data_={} #Creating a dictionary for the CSV headers
    field_names=['Source']
    field_names.append('Page')
    [field_names.append('B' + str(i)) for i in range(50)]

    CSV_Dir=WDir + 'PDFs.csv'

    if not path.exists(CSV_Dir): #Create the CSV file and add the headers 
        with open(CSV_Dir, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(field_names)
            f.close()

    with open(WDir + FName + '.pdf', "rb") as pdf: #Open the PDF file
        inputpdf=PdfReader(pdf)

        for i in range(len(inputpdf.pages)): #iterat through the PDF pages and create a seperate tem PDF file for each page
            output = PdfWriter()
            output.add_page(inputpdf.pages[i])
            with open(FName + '_'+  str(i) + '.pdf', "wb") as outputStream:
                output.write(outputStream)

            with open(FName + '_'+  str(i) + '.pdf', "rb") as Tempfile: #Open the temp PDF files and extract the contents into base64 code
                my_string=base64.b64encode(Tempfile.read())
                my_string=my_string.decode('ascii')
                
            os.remove(FName + '_' + str(i) + '.pdf') #delete the tem files

            if i<9: n="00" + str(i+1)
            elif i<99: n="0" + str(i+1)
            else: n=str(i+1)
            
            with open(CSV_Dir, 'a',encoding="UTF8") as f: #add the PDF base64 code into the CSV file
                NRow = DictWriter(f, fieldnames=field_names, lineterminator = '\n')
                Data_={'Source':FName,'Page':'Page' + n}
                for j in range(int(len(my_string)/32000)+1): #break the base64 code into portions of 32000 charachters before saving them into the CSV file to avoid the characters length limitation
                    Data_['B' + str(j)]=my_string[j*32000:(j+1)*32000]
                NRow.writerow(Data_)

WDir="C:\\Users\\hamze\\Desktop\\NG BI Guru\\Video contents\\PDF Videos\\Video 2 PDF search\\" #Make sure to replace / with // for python to treat the text as a directory (Path)
for file in os.listdir(WDir): #iterate through the PDF files in the directory and extract the contents to the CSV file
    if os.path.isfile(os.path.join(WDir, file)) and file.lower().endswith(".pdf"):              
        FlN=file.rsplit( ".", 1 )[ 0 ]
        ProcessPDF(WDir,FlN)
