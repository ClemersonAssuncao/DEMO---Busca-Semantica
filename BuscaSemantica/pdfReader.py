import os
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re

class PdfReader:

    def __init__(self, instance):
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
    
    
    def get_json_file(self):
        json_data = []
        
        def remove_word_break(value):
            return ' '.join(value.strip().splitlines())

        # Preparação para Embedding do arquivo
        if (self.instance.file and os.path.exists(self.instance.file.path)):
            with open(self.instance.file.path, 'rb') as file:
                for paragrafo in re.split(r"[;.]", self.converter(file).strip()):
                    paragrafo_tratado = remove_word_break(paragrafo)
                    if (len(paragrafo_tratado.split(' ')) > 3):
                        json_data.append({
                            'id': self.instance.id,
                            'text': paragrafo_tratado,
                            'type': 'file'
                        })
        return json_data
    
    def get_json_instance(self):
        def remove_word_break(value):
            return ' '.join(value.strip().splitlines())
        json_data = []
        # Preparação para Embedding do name
        json_data.append({
                        'id': self.instance.id,
                        'text': self.instance.name,
                        'type': 'name'
                    })
        
        # Preparação para Embedding do description
        description = remove_word_break(self.instance.description) 
        if (description):
            json_data.append({
                            'id': self.instance.id,
                            'text': description,
                            'type': 'description'
                        })
        return json_data