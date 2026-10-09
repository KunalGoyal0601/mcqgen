#utils file is a helper file what ever helper funtion write it down over here
import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endwith('pdf'):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

        except Exception as e:
            raise Exception('Error in reading pdf file')
        
    elif file.name.endwith('txt'):
        return file.read().decode('utf-8')
    
    
    
    else:
        raise Exception("unsupported file")
    

#3def get_table_data():

