import os
from connection import ( connect_watsonx_embedding, connect_sentencetransformer,connect_watsonx_llm, connect_to_milvus)
from __generate_answer.function import ( embedding_data ,find_answer_doc_from_q_df, generate_doc, 
                                                        drop_milvus_collection, split_text_with_overlap )
import pandas as pd
from utils.config import settings

# embedding model
model_embedder_source = settings.generate_answer.embedder_model.source
model_id_embedder =     settings.generate_answer.embedder_model.name

if model_embedder_source == 'watsonxai':
    model_embedder = connect_watsonx_embedding(model_id_embedder)
elif model_embedder_source == 'huggingface':
    model_embedder = connect_sentencetransformer(model_id_embedder)

chunk_size=         settings.generate_answer.embedder_model.chunk_size
overlap_size=       settings.generate_answer.embedder_model.overlap_size

# large language model
model_id_llm=       settings.generate_answer.llm_generate.name
decoding_method=    settings.generate_answer.llm_generate.decoding_method
min_new_tokens=     settings.generate_answer.llm_generate.min_new_tokens
max_new_tokens=     settings.generate_answer.llm_generate.max_new_tokens
repetition_penalty= settings.generate_answer.llm_generate.repetition_penalty

model_llm  = connect_watsonx_llm(model_id_llm, 
                                 decoding_method, min_new_tokens, max_new_tokens, repetition_penalty)

file_location = settings.generate_answer.question_csv_location
file_name = settings.generate_answer.question_csv_name

# create question dataframe 
question_df = pd.read_csv(f'{file_location}{file_name}')
print(f'generating answer from {file_location}{file_name}')
print(f'with {model_id_llm}')

# --- from text
# make sure to run `milvus-server --proxy-port 19530` command in terminal to connect to milvus lite
connect_to_milvus()
thai_text = open("text/leave_policy_TH.txt", encoding="utf8").read()
chunks = split_text_with_overlap(thai_text, chunk_size, overlap_size)
collection = embedding_data(chunks, model_embedder)
hits = find_answer_doc_from_q_df(question_df, collection, model_embedder)
generate_doc(question_df, hits)

content_df = question_df.loc[:,['question','contexts']]

print('exporting csv file...')
content_df.to_csv(f'{file_location}/content.csv')
content_df.to_excel(f'{file_location}/excel/content.xlsx')

drop_milvus_collection()