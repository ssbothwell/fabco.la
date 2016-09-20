from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter, A4, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from work.models import Client, Project, LineItem
import re, textwrap

class MyPrint:
    def __init__(self, buffer, pagesize, pk):
        self.pk = pk
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def _header_footer(self, canvas, doc):
        """ Renders a header and footer which will be inserted regardless of pdf method"""
        
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        stylesheet = getSampleStyleSheet()
 
        # Header
        logo = Image("http://www.fabco.la/fabco-seal-1.png", width=1.5*inch, height=1.5*inch)
        logo.hAlign = 'CENTER'
        
        stylesheet['BodyText'].fontSize = 10    
        stylesheet['BodyText'].leading = 14
        stylesheet['BodyText'].leftIndent = 5
        stylesheet['BodyText'].textColor = 'gray'
        
        FabcoAddress = "Fabco Art Services\n166 West Avenue 34\nLos Angeles CA 90031"
                                       
                                       
        project = get_object_or_404(Project, pk=self.pk)
        rightHeader = "Job #%s\nCompletion Date %s" % (project.project_id, project.due_date)
        
        # Build and format Left Header Table:
        leftHeaderData = [[FabcoAddress],
                            [project.client.first_name + ' ' + project.client.last_name+'\n'+project.client.address.street+'\n'+project.client.address.city + ' ' + project.client.address.zip_code], 
                            ]
        leftHeaderTable = Table(leftHeaderData)
        leftHeaderTable.setStyle(TableStyle([
                                            ('LEFTPADDING',(0,0),(0, 1),0),
                                            ('TOPPADDING',(0,1),(0, 1), 30),
                                            ('BOTTOMPADDING',(0,1),(0, 1), 0),                                            
                                            ]))

        # Build and format Header Table:
        headerData = [([leftHeaderTable, logo, rightHeader])]
        headerTable = Table(headerData, colWidths=doc.width/3)
        headerTable.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-3, 0), 'MIDDLE'),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
            ('ALIGN',(1,0),(1,0),'CENTER'),
            ('ALIGN',(2,0),(2,0),'RIGHT'),
            ('LEFTPADDING',(0,0),(0,0),-1),
            ('RIGHTPADDING',(2,0),(2,0),-1),        
            ]))
        
        
        # find required space | I don't really understand this..    
        w, h = headerTable.wrap(doc.width, doc.height)
        # render to canvas | I also don't really understand this..
        headerTable.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - doc.bottomMargin) 
 
        # Footer
        footer = Paragraph('Client Signature: _________________________', stylesheet['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin)
 
        # Release the canvas
        canvas.restoreState()

    def print_quote(self):
        """ Render the quote PDF """
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=1 * inch,
                                leftMargin=1 * inch,
                                topMargin=2 * inch,
                                bottomMargin=1 * inch,
                                pagesize=self.pagesize,
                                showBoundary=0)
 
        # Our container for 'Flowable' objects
        elements = []
 
        # A large collection of style sheets pre-made for us
        stylesheet = getSampleStyleSheet()
        stylesheet.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
 
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        project = get_object_or_404(Project, pk=self.pk)
        lineitems = project.line_item.all()
        
        # Parse lineitems and put into list [(name, description2),(name2, description2)]
        data = [('Name', 'Description', 'Unit Cost', 'Quantity', 'Total')]
        for lineitem in lineitems:
            if len(lineitem.description) > 63:                
                lineitem.description = textwrap.fill(lineitem.description, 38)
                
            lineitem.description = "\n".join(lineitem.description.splitlines())
            
            item = (Paragraph(lineitem.name, stylesheet['Normal']), lineitem.description, '$' + str(lineitem.price), lineitem.quantity, lineitem.tallys['total'])
            data.append(item)
        
        totalsData = [('','','','Sub-Total', project.sub_total),('','','','Tax', project.tax), ('','','','Total', project.total)]
            
        table = Table(data, colWidths=(doc.width/5,2*doc.width/5,0.6667*doc.width/5,0.6667*doc.width/5,0.6667*doc.width/5))
        table.setStyle(TableStyle([('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        
        totalsTable = Table(totalsData, colWidths=(doc.width/5,2*doc.width/5,0.6667*doc.width/5,0.6667*doc.width/5,0.6667*doc.width/5))
        totalsTable.setStyle(TableStyle([
            ('LINEABOVE',(3,0),(4,0),1,colors.black),
            ('INNERGRID', (3, 0), (4, 2), 0.25, colors.black),
            ('BOX', (3, 0), (4, 2), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ]))
        
        # Insert content tables and build doc
        elements.append(Spacer(1,.5*inch))
        elements.append(table)
        elements.append(totalsTable)
        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
        
    def print_work_order(self):
        """ Render the quote PDF """
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=1 * inch,
                                leftMargin=1 * inch,
                                topMargin=2 * inch,
                                bottomMargin=1 * inch,
                                pagesize=self.pagesize,
                                showBoundary=0)
 
        # Our container for 'Flowable' objects
        elements = []
 
        # A large collection of style sheets pre-made for us
        stylesheet = getSampleStyleSheet()
        stylesheet.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
 
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        project = get_object_or_404(Project, pk=self.pk)
        lineitems = project.line_item.all()
    
        # Parse lineitems and put into list [(name, description2),(name2, description2)]
        data = [('Name', 'Description', 'Quantity')]
        for lineitem in lineitems:
            
            if len(lineitem.description) > 63:                
                lineitem.description = textwrap.fill(lineitem.description, 64)
                
            lineitem.description = "\n".join(lineitem.description.splitlines())
            item = (Paragraph(lineitem.name, stylesheet['Normal']), lineitem.description, lineitem.quantity)
            
            data.append(item)
    
        
        table = Table(data, colWidths=(doc.width/5, None,0.75*inch))
        table.setStyle(TableStyle([('INNERGRID', (0, 1), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
    

        # Insert content tables and build doc
        elements.append(Spacer(1,.5*inch))
        elements.append(table)
        doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf