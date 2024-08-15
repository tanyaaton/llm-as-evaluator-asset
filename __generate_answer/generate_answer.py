import pandas as pd
from connection import ( connect_watsonx_llm, connect_sentencetransformer, connect_to_milvus, connect_watsonx_llm_w_2)
from __generate_answer.function import ( find_response_openai, find_response )
from utils.config import settings
from openai import OpenAI


# large language model
model_source=       settings.generate_answer.llm_generate.source
model_id_llm=       settings.generate_answer.llm_generate.name
decoding_method=    settings.generate_answer.llm_generate.decoding_method
min_new_tokens=     settings.generate_answer.llm_generate.min_new_tokens
max_new_tokens=     settings.generate_answer.llm_generate.max_new_tokens
repetition_penalty= settings.generate_answer.llm_generate.repetition_penalty

file_location = settings.generate_answer.question_csv_location
file_name = settings.generate_answer.question_csv_name

# create question dataframe 
question_df = pd.read_csv(f'{file_location}{file_name}')
print(f'generating answer from {file_location}{file_name}')
print(f'with {model_id_llm}')

# --- from dataframe
content_df = question_df.loc[:,['question','contexts']]

if model_source == 'watsonxai':
    model_llm  = connect_watsonx_llm_w_2(model_id_llm, 
                                 decoding_method, max_new_tokens, min_new_tokens, [']'],repetition_penalty)
    find_response(model_llm, content_df)

elif model_source == 'openai':
    client = OpenAI()
    find_response_openai(client, model_id_llm, content_df)

elif model_source == 'huggingface':
    model_llm = connect_sentencetransformer(model_id_llm)
    print(model_llm)

print('exporting csv file...')
content_df.to_csv(f'{file_location}/content.csv')
content_df.to_excel(f'{file_location}/excel/content.xlsx')