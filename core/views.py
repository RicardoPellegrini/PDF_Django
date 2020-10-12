# Usando ReportLab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.views.generic import View

# Usando WeasyPrint
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import HttpResponse

from weasyprint import HTML


class IndexView(View):

  def get(self, request, *args, **kwargs):
    # Cria um arquivo para receber os dados e gerar o PDF
    buffer = io.BytesIO()

    # Cria o arquivo PDF
    pdf = canvas.Canvas(buffer)

    # Insere dados no PDF
    pdf.drawString(100, 100, "Geek University")

    # Quando acabamos de inserir dados no PDF
    pdf.showPage()
    pdf.save()

    # Retornar o buffer ao início do arquivo
    buffer.seek(0)

    # # Faz o download do pdf gerado
    # return FileResponse(buffer, as_attachment=True, filename='relatorio1.pdf')

    # Abre o pdf direto no navegador
    return FileResponse(buffer, filename='relatorio1.pdf')


class Index2View(View):

  def get(self, request, *args, **kwargs):
    texto = ['Geek University', 'Evolua seu lado Geek', 'Programação Web com Python e Django']

    html_string = render_to_string('relatorio.html', {'texto': texto})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/relatorio2.pdf')

    fs = FileSystemStorage('/tmp')

    with fs.open('relatorio2.pdf') as pdf:
      response = HttpResponse(pdf, content_type='application/pdf')
      response['Content-Disposition'] = 'inline; filename="relatorio2.pdf"'
    
    return response
