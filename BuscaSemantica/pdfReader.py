import os
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re

class PdfReader:

    def __init__(self, instance):
        if not os.path.exists(instance.file.path):
            raise Exception(f'Arquivo Inexistente: {instance.file}')
        self.instance = instance

    def converter(self, file):
        
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
        converter.close()
        text = output.getvalue()
        output.close()
        return text 
    
    def get_json_text(self):

        def remove_word_break(value):
            return ' '.join(value.strip().splitlines())
        
        json_data = [{
                        'id': self.instance.id,
                        'name': self.instance.name, 
                        'description': self.instance.description,
                        'file_name': os.path.basename(file.name),
                        'file_text': self.instance.description
                    },
                    {
                        'id': self.instance.id,
                        'name': self.instance.name, 
                        'description': self.instance.description,
                        'file_name': os.path.basename(file.name),
                        'file_text': self.instance.name
                    },]
        with open(self.instance.file.path, 'rb') as file:
            for paragrafo in re.split(r"[;.]", self.converter(file).strip()):
                paragrafo_tratado = remove_word_break(paragrafo)
                if (len(paragrafo_tratado.split(' ')) > 3):
                    json_data.append({
                        'id': self.instance.id,
                        'name': self.instance.name, 
                        'description': self.instance.description,
                        'file_name': os.path.basename(file.name),
                        'file_text': paragrafo_tratado
                    })
        return json_data