
import openai
from openai.embeddings_utils import cosine_similarity
from django.conf import settings
import pandas as pd
from .pdfReader import PdfReader

class OpenIAService:

    def __init__(self):
        openai.api_key = settings.OPEN_IA_TOKEN 
        self.EMBEDDING_ENGINE = 'text-embedding-ada-002'

    def __get_data_frame_file(self):
        try:
            return pd.read_csv(settings.DF_FILE_NAME)
        except pd.errors.EmptyDataError:
            return None
        except FileNotFoundError:
            return pd.DataFrame(columns=['id', 'type', 'text'])

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

    def appendFile(self, instance):
        json_data = PdfReader(instance).get_json_file()
        df_new = pd.DataFrame(json_data)
        # df_new['ada_embedding'] = df_new['text'].apply(lambda x: self.get_embedding(x))
        
        df = self.__get_data_frame_file()
        df = df.drop(df[(df['id'] == instance.id) & (df.type == 'file')].index)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(settings.DF_FILE_NAME, index=False)

    def appendInstance(self, instance):
        json_data = PdfReader(instance).get_json_instance()
        df_new = pd.DataFrame(json_data)
        # df_new['ada_embedding'] = df_new['text'].apply(lambda x: self.get_embedding(x))
        df = self.__get_data_frame_file() 
        df = df.drop(df[(df['id'] == instance.id) & ((df.type == 'description') | (df.type == 'name'))].index)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(settings.DF_FILE_NAME, index=False)
    
        
    def deleteInstance(self, instance):
        df = pd.read_csv(settings.DF_FILE_NAME)
        df = df.drop(df[df.id == instance.id].index)
        df.to_csv(settings.DF_FILE_NAME, index=False)

