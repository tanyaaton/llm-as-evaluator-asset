from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames
from langchain_ibm import WatsonxEmbeddings
from ibm_watsonx_ai.foundation_models import Model
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from pymilvus import connections

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY", None)
project_id = os.environ["PROJECT_ID"]
ibm_cloud_url = os.environ["IBM_CLOUD_URL"]
api_key = os.environ["WATSONX_APIKEY"]
openai_key = os.environ["OPENAI_API_KEY"]

if api_key is None or ibm_cloud_url is None or project_id is None:
    print("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
else:
    creds = {
        "url": ibm_cloud_url,
        "apikey": api_key 
    }

def connect_watsonx_embedding(model_id_embedding):
    embed_params = {
            EmbedTextParamsMetaNames.TRUNCATE_INPUT_TOKENS: 3,
            EmbedTextParamsMetaNames.RETURN_OPTIONS: {"input_text": True},
        }
    print('connecting to watsonxembedding...')
    watsonx_embedding = WatsonxEmbeddings(
            model_id=model_id_embedding,
            url=ibm_cloud_url,
            project_id=project_id,
            params=embed_params,
        )
    return watsonx_embedding

def connect_sentencetransformer(model_id_embedding):
    print('connecting to sentencetranformerembedding...')
    sentencetransformer_embedding = SentenceTransformer(f'{model_id_embedding}')
    return sentencetransformer_embedding

def connect_watsonx_llm(model_id_llm, decoding_method, min_new_tokens, max_new_tokens, repetition_penalty):
    print('connecting to watsonxllm...')
    params = {
        'decoding_method': decoding_method,
        'min_new_tokens': min_new_tokens,
        'max_new_tokens': max_new_tokens,
        # "stop_sequences": stop_sequences,
        'temperature': 0.0,
        'repetition_penalty': repetition_penalty
    }
    model_llm = Model(model_id= model_id_llm,
                    params=params, credentials=creds,
                    project_id=project_id)
    
    return model_llm

def connect_watsonx_llm_w_2(model_id_llm, decoding_method, max_new_tokens, min_new_tokens, stop_sequences, repetition_penalty):
    print('connecting to watsonxllm...')
    print('ss', stop_sequences)
    params = {
        "decoding_method": decoding_method,
        "max_new_tokens": max_new_tokens,
        "min_new_token": min_new_tokens,
        "stop_sequences": stop_sequences,
        "repetition_penalty": repetition_penalty
    }
    print('params', params)
    model_llm = Model(model_id= model_id_llm,
                    params=params, credentials=creds,
                    project_id=project_id)
    return model_llm


def connect_to_milvus():
    print('connecting to milvus...')
    connections.connect(host= 'localhost', port='19530')