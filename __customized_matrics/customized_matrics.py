# from connection import read_json_file, read_text_file, recording_results_to_csv
from utils.config import settings
from connection import connect_watsonx_llm, connect_watsonx_llm_w_2
from __customized_matrics.prompt import prompt_generation
from prompt_template import get_prompt_template
import time
import requests
import pandas as pd
import datetime
import numpy as np

# llm evaluation model
e_model_id=             settings.customized_matrics.llm_eval.name
e_decoding_method=      settings.customized_matrics.llm_eval.decoding_method
e_min_new_tokens=       settings.customized_matrics.llm_eval.min_new_tokens
e_max_new_tokens=       settings.customized_matrics.llm_eval.max_new_tokens
e_repetition_penalty=   settings.customized_matrics.llm_eval.repetition_penalty
e_mode=                 settings.customized_matrics.llm_eval.prompt_language
e_model_source=         settings.customized_matrics.llm_eval.source
e_stop_token =          ["]"]

if e_model_source == 'watsonxai':
    eval_model  = connect_watsonx_llm_w_2(e_model_id, 
                                 e_decoding_method, e_max_new_tokens, e_min_new_tokens, e_stop_token, e_repetition_penalty)
elif e_model_source == 'openai':    pass
else:   raise ValueError(f"Invalid input: '{e_model_source}' model is not supported. Pleasechoose model from 'watsonxai' or 'openai' sources")

file_location = settings.customized_matrics.content_csv_location
file_name = settings.customized_matrics.content_csv_name
file_groundtruth_location = settings.customized_matrics.ground_truth_csv_location
print(f'evaluating {file_location}{file_name} with {e_model_id}')

data_df = pd.read_csv(f'{file_location}{file_name}')
content_df = data_df.loc[:,["question","answer","contexts"]]
data_gt_df = pd.read_csv(f'{file_groundtruth_location}')
content_df["groundtruth"] = data_gt_df.groundtruth

now = datetime.datetime.now()
formatted_datetime = now.strftime("%d-%m-%Y_%H%M")
start = time.time()

new_df = content_df
for i in content_df.index:
    print('-------',i,'-------')
    answer = content_df.loc[i,'answer']
    context = content_df.loc[i,'contexts']
    groundtruth = content_df.loc[i,'groundtruth']
    question = content_df.loc[i,'question']

    message = prompt_generation(context, question, groundtruth, answer)
    prompt = get_prompt_template(eval_model, message)
    print('--prompt--')
    response = eval_model.generate_text(prompt)
    print('r-',response)
    new_df.loc[i,'response'] = int(response[0])

end = time.time()
total_time_taken = end - start
# print(total_time_taken)

mean_df = new_df.loc[:,["response"]].dropna()
mean_array = mean_df.to_numpy()
mean = round(np.average(mean_array),5)
print('customized metric score = ', mean)

print('exporting csv...')
new_df.to_csv(f'{file_location}/eval_customized_metrics_{formatted_datetime}.csv')
new_df.to_csv(f'{file_location}/eval_customized_metrics_{formatted_datetime}.csv')



# recording_results_to_csv(qa_data, responses, 'mpt-30b', 'used mpt-30b, and no trans', "EN", total_time_taken, 'results/qa_answer_mpt-30b.csv')
# recording_results_to_csv(qa_data, responses, name, '', "", total_time_taken, f'scoring-llama3/{name}.csv')