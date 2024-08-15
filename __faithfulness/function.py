import pandas as pd
import logging
import datetime
import ast
from __faithfulness.prompt import ( faithfulness_divide_answer_prompt_EN, 
                                   faithfulness_evaluation_prompt_EN )
from prompt_template import get_prompt_template


now = datetime.datetime.now()
formatted_datetime = now.strftime("%d-%m-%Y_%H%M")
logging.basicConfig(filename=f'log/faithfulness_{formatted_datetime}.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


def store_divided_answer_found(df, divide_model, d_mode, eval_model, e_mode):
    ii=0
    new_df = pd.DataFrame()
    for i in df.index:
        yes_count = 0
        no_count = 0
        print('****************')
        print('question no:', i)
        # get faithfulness prompt
        message_d = faithfulness_divide_answer_prompt_EN(df.loc[i,'answer'])
        prompt_d = get_prompt_template(divide_model, message_d)
        logging.info(prompt_d)
        print('prompt-D', prompt_d)
        # generate response
        response_d = divide_model.generate_text(prompt_d)
        print('--response--',response_d)
        # reformat the response
        response_d = '["' + response_d +']'
        logging.info(response_d)
        # divided_answers_list = ast.literal_eval(response_d)
        try:
        # Attempt to convert the string to a list
            divided_answers_list = ast.literal_eval(response_d)
        
        # Check if the result is indeed a list
            if isinstance(divided_answers_list, list):
                print("Converted list:", divided_answers_list)
            else:
                divided_answers_list = ['']
        except (SyntaxError, ValueError):
            divided_answers_list = ['']
        # store the divided answer
        new_df.loc[ii,'question_no']=i
        new_df.loc[ii,'answer']=df.loc[i,'answer']
        new_df.loc[ii,'question']=df.loc[i,'question']
        new_df.loc[ii,'contexts']=df.loc[i,'contexts']
        ii_freeze = ii
        for divided_answer in divided_answers_list:
            new_df.loc[ii,'divided_answer']=divided_answer
            message_e = faithfulness_evaluation_prompt_EN(context=df.loc[i,'contexts'], answer=divided_answer)
            prompt_e = get_prompt_template(eval_model, message_e)
            # print('prompt-E', prompt_e)
            logging.info(prompt_e)
            response_e = eval_model.generate_text(prompt_e)
            logging.info(response_e)
            new_df.loc[ii,'llama3_label']=response_e
            ii+=1
            print(response_e[0])
            if ('0' in response_e[0]):
                no_count += 1
            elif ('1' in response_e[0]):
                yes_count  += 1
        new_df.loc[ii_freeze,"faithfuln"]=yes_count/(yes_count+no_count)
        new_df.loc[ii_freeze,"yes_count"]=yes_count
        new_df.loc[ii_freeze,"no_count"] =no_count
        print(i, ';',yes_count, no_count )
    return new_df