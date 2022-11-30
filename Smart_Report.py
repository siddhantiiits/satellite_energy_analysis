from fpdf import FPDF
from datetime import datetime
import os
import shutil
def generateReport(rec):
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font('Arial', 'B', 12)
    # pdf.cell(40, 20, 'Generated On: '+ str(datetime.now()))
    # pdf.output('London SPR Generated on: '+str(datetime.now())+'.pdf', 'F')
    shutil.copy('Satellite Images/Delhi/rp.pdf','London Smart Report Generated on: '+str(datetime.now())+'.pdf')

