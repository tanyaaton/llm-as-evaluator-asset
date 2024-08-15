import pandas as pd
import numpy as np
import ast
import logging
from utils.config import settings
from __answer_relevancy.function import npsumdot_3d
from __answer_relevancy.prompt import answer_relevancy_predict_questions_prompt_EN
from connection import ( connect_watsonx_embedding, connect_sentencetransformer, connect_watsonx_llm, connect_watsonx_llm_w_2)
from prompt_template import get_prompt_template
import datetime

# IBM embedding (en)
model_embedder_source = settings.answer_relevancy.embedder_model.source
model_id_embedder =     settings.answer_relevancy.embedder_model.name

if model_embedder_source == 'watsonxai':
    model_embedder  =     model_embedder = connect_watsonx_embedding(model_id_embedder)
elif model_embedder_source == 'huggingface':
    model_embedder  =     model_embedder = connect_sentencetransformer(model_id_embedder)
else:   raise ValueError(f"Invalid input: '{model_embedder_source}' model is not supported. Pleasechoose model from 'watsonxai' or 'openai' sources")


# choose llm IBM model for predict question model
p_model_id=             settings.answer_relevancy.llm_predict.name
p_decoding_method=      settings.answer_relevancy.llm_predict.decoding_method
p_min_new_tokens=       settings.answer_relevancy.llm_predict.min_new_tokens
p_max_new_tokens=       settings.answer_relevancy.llm_predict.max_new_tokens
p_repetition_penalty=   settings.answer_relevancy.llm_predict.repetition_penalty
# p_mode=                 settings.answer_relevancy.llm_predict.prompt_language
p_model_source=         settings.answer_relevancy.llm_predict.source
p_stop_token =          ["]"]

if p_model_source == 'watsonxai':
    predict_model  =     connect_watsonx_llm_w_2(p_model_id, 
                                 p_decoding_method, p_max_new_tokens, p_min_new_tokens, p_stop_token, p_repetition_penalty)
else:   raise ValueError(f"Invalid input: '{p_model_source}' model is not supported. Please choose model from 'watsonxai' sources")


file_location = settings.answer_relevancy.content_csv_location
file_name = settings.answer_relevancy.content_csv_name
print(f'evaluating {file_location}{file_name} with {p_model_id}')

content_df = pd.read_csv(f'{file_location}{file_name}')
new_df = content_df.loc[:,["question","answer","contexts"]]

predict_q_list = []
for i in content_df.index:
    answer = content_df.loc[i,'answer']
    # predicted_question = predict_question_from_answer_llm3_TH(answer, predict_model, 'EN')
    message_p = answer_relevancy_predict_questions_prompt_EN(answer)
    prompt_p = get_prompt_template(predict_model, message_p)
    response_p = predict_model.generate_text(prompt_p)
    print('r-',response_p)
    response_p = '["' + response_p +']'
    response_q_list = ast.literal_eval(response_p)
    predict_q_list.append(response_q_list)
    logging.info(response_p)
    print('prompt---', prompt_p)
    print('reponse---', response_p)
    new_df.loc[i,'predicted_question'] = response_p

original_q  = new_df.question.values.tolist()
# predicted_q = new_df.predicted_question.values.tolist()

embeddings_list = []
# Generate embeddings for each text in each sublist and store them in the list
for sublist in predict_q_list:
    sublist_embeddings = []
    print(type(sublist))
    print('eln',len(sublist))
    for text in sublist:
        print(text)
        embedding = model_embedder.encode(text)
        sublist_embeddings.append(embedding)
    print(len(sublist_embeddings))
    embeddings_list.append(sublist_embeddings)

embeddings_array = np.array(embeddings_list)

if model_embedder_source == 'huggingface':
    vector_orig = np.array(model_embedder.encode(original_q))

#----norm
print(vector_orig.shape) #(11, 768)
norm_oq = np.linalg.norm(vector_orig, axis=1)
print(norm_oq)           #(11,)
print(norm_oq.shape)
#repeat original question
array_2d = np.repeat(norm_oq[:, np.newaxis], repeats=3, axis=1)
print(array_2d)         #(11, 3)


print(embeddings_array.shape)
norm_epq = np.linalg.norm(embeddings_array, axis=2)
print(norm_epq)
print(norm_epq.shape)

norm = norm_epq * array_2d

#----product
array_2d_org = np.repeat(vector_orig[:, np.newaxis], repeats=3, axis=1)
print(array_2d_org)

dot_product = npsumdot_3d(array_2d_org, embeddings_array)

#answer relevancy

answer_relevancy_array = dot_product / norm
row_averages = np.mean(answer_relevancy_array, axis =1)
new_df['answer_relevancy']=row_averages
content_df['answer_relevancy']=row_averages

mean_all = round(np.average(answer_relevancy_array),5)
print('answer_relevancy = ', mean_all)

now = datetime.datetime.now()
formatted_datetime = now.strftime("%d-%m-%Y_%H%M")

new_df.to_csv(f'{file_location}eval_ansrelevancy_{formatted_datetime}.csv')
new_df.to_excel(f'{file_location}excel/eval_ansrelevancy_{formatted_datetime}.xlsx')
content_df.to_csv(f'{file_location}eval_ansrelevancy_detial_{formatted_datetime}.csv')
content_df.to_excel(f'{file_location}excel/eval_ansrelevancy_detial_{formatted_datetime}.xlsx')