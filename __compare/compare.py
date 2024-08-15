import pandas as pd
from utils.config import settings
import numpy as np

file_name_list =  settings.compare.file_name_list
file_location = settings.compare.file_location
metric_name = settings.compare.metric
print(file_name_list)

if metric_name == 'faithfulness':
    column_name = 'faithfuln'
elif metric_name == 'answer_relevancy':
    column_name = 'answer_relevancy'
elif metric_name == 'customized_matrics':
    column_name = 'response'
else: 
    raise ValueError(f"Invalid input: '{metric_name}' metric is not supported. Please choose model from [faithfulness, answer_relevancy, customized_matrics]")


with open(f'{file_location}/compare_{metric_name}.txt', 'w') as f:
    for i in file_name_list:
        data_df = pd.read_csv(f'{file_location}{i}')
        print(i)
        # mean = round(float(data_df.loc[:,["faithfuln"]].mean()),3)
        mean_df = data_df.loc[:,[f"{column_name}"]].dropna()
        mean_array = mean_df.to_numpy()
        mean = round(np.average(mean_array),5)
        print(mean)
        f.write(i[:-20]+'\n')
        f.write(f'faithfulness mean = {mean}\n')