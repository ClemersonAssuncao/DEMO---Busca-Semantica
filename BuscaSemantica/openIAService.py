
import openai
from openai.embeddings_utils import cosine_similarity
from django.conf import settings
import pandas as pd
from .pdfReader import PdfReader

class OpenIAService:

    def __init__(self):
        openai.api_key = settings.OPEN_IA_TOKEN 
        self.EMBEDDING_ENGINE = 'text-embedding-ada-002'

    def get_embedding(self,text_to_embed):
        response = openai.Embedding.create(
            model= self.EMBEDDING_ENGINE,
            input=[text_to_embed]
        )
        embedding = response["data"][0]["embedding"]
        return embedding
    
    def search(self, text, dataFrame):
        embedding = self.get_embedding(text)
        dataFrame['similarities'] = dataFrame.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
        res = dataFrame.sort_values('similarities', ascending=False)
        return res

    def appendInstance(self, instance):
        json_data = PdfReader(instance).get_json_text()
        df_new = pd.DataFrame(json_data)
        df_new['ada_embedding'] = df_new['file_text'].apply(lambda x: self.get_embedding(x))
        
        try:
            df = pd.read_csv(settings.DF_FILE_NAME)
            df = df.drop(df[df.id == instance.id].index)
            df_outer = pd.concat([df, df_new], ignore_index=True)
        except pd.errors.EmptyDataError:
            df_outer = df_new
        df_outer.to_csv(settings.DF_FILE_NAME, index=False)

        


    def deleteInstance(self, instance):
        df = pd.read_csv(settings.DF_FILE_NAME)
        df = df.drop(df[df.id == instance.id].index)
        df.to_csv(settings.DF_FILE_NAME, index=False)

