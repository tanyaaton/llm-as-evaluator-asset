# 📊 LLM as evaluator

## STEP 1: SET UP

This lab implement `llama-3-1-70b` model to use as evaluator for RAG application
Before getting start, please follow these steps
1. Install all the requirement package<br/>
    ```
   pip install -r requirements.txt
    ```
3. Install utils by running this command<br/>
    ```
   pip install -e .
    ```
5. add `.env` file with credential for ibm watsonx (following the env_template)

## STEP 2: SPECIFY MODEL

In folder `configs`, you will find a `setting.yaml` file which contain all the model speccification for running evaluation.
The detail of this file will be changed according to your folder name and file name that contain the data you want to evaluate.<br/>
<br/>

## STEP 3: GENERATE ANSWER FROM LLM MODEL

### 📌 -------- Generate Answer --------
**Input** ➡️ `.csv` file, contains Dataframe with column `["question", "contexts"]`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **"question"**: list of questions that is used for the LLM to generate the answer<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **"contexts"**: contexts that is retrieve from RAG application, and used as knowledge to answer the above questions<br/>
**Output** ➡️  `content.csv` file, contains Dataframe with column `["question", "contexts", "answer"]`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **"answer"**: the answer generate by LLM that will be evaluated, using question and context above<br/>


#### generate_answer.py
To run this function
1. Create a folder. The name should be related to the model you will be used to generate answer (eg. `csv_hr_gpt4`)
2. Store your Input Dataframe in the folder (.csv file that contain `["question", "contexts"]` )
3. In the `setting.yaml` file, store your `question_csv_location` and `question_csv_name` 
4. In the `setting.yaml` file, choose the language model (LLM) for generating questions and its source in `llm_generate.source`and `llm_generate.name`. This model will later be evaluated by LLaMA 3.1 70B in the future.<br/><br/>


## STEP 3: RUNNING THE EVALUATOR


### 📌 -------- Faithfulness --------

**Input** ➡️ `conent.csv` file, contains Dataframe with column `["question", "contexts", "answer]` (generated from `generate_answer.py`)<br/>
<br/>
**Output** ➡️  `eval_faithfulness_xx-xx-xxxx_xxxx.csv` file, and `eval_faithfulness_detail_xx-xx-xxxx_xxxx.csv` file <br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_faithfulness_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "faithfuln"]` <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"faithfuln" being the score from 0-1 of the `content.csv`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_faithfulness_detail_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "divided_answer", "faithfuln"]`<br/>

**faithfulness.py**<br/>
To run this function
1. In the `setting.yaml` file, in the `faithfulness` session
&nbsp;&nbsp;&nbsp;&nbsp;1.1 Store your `content_csv_location` and `content_csv_name` of the **content.csv** file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.2 In the `llm_divide' and `llm_eval` session, you can choose the model `source` and `name` you want to use for evaluating the content.csv (default model is llama3.1 70B )<br/>
2. Go to your terminal
3. cd in to the `llm-as-evaluator-main` folder
4. run the following command to evaluated faitfulness<br/>
```
python __faithfulness/faithfulness.py
```
<br/>
After run faithfulness.py, `eval_faithfulness_xx-xx-xxxx_xxxx.csv` and `eval_faithfulness_detail_xx-xx-xxxx_xxxx.csv` will be generated in the folder specified


### 📌 -------- Answer Relevancy --------

**Input** ➡️ `conent.csv` file, contains Dataframe with column `["question", "contexts", "answer]` (generated from `generate_answer.py`)<br/>
<br/>
**Output** ➡️  `eval_ansrelevancy_xx-xx-xxxx_xxxx.csv` file, and `eval_ansrelevancy_detail_xx-xx-xxxx_xxxx.csv` file <br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_ansrelevancy_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "answer_relevancy"]` <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"answer_relevancy" being the score from 0-1 of the `content.csv`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_ansrelevancy_detail_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "predicted_answer", "answer_relevancy"]`<br/>

**answer_relevancy.py**<br/>
To run this function
1. In the `setting.yaml` file, in the `answer_relevancy` session
&nbsp;&nbsp;&nbsp;&nbsp;1.1 Store your `content_csv_location` and `content_csv_name` of the **content.csv** file
&nbsp;&nbsp;&nbsp;&nbsp;1.2 In the `embedder_model` session, you can choose the model `source` and `name` you want to use for embedding (default model is kornwtp/simcse-model-phayathaibert from huggingface )<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.3 In the `llm_eval` session, you can choose the model `source` and `name` you want to use to evaluate the content.csv (default model is llama3.1 70B )<br/>
3. Go to your terminal
4. cd in to the `llm-as-evaluator-main` folder
5. run the following command to evaluated faitfulness<br/>
```
python __answer_relevancy/answer_relevancy.py
```
<br/>
After run answer_relevancy.py, `eval_ansrelevancy_xx-xx-xxxx_xxxx.csv` and `eval_ansrelevancy_detail_xx-xx-xxxx_xxxx.csv` will be generated in the folder specified


### 📌 -------- Customize Metric --------
**Input** ➡️ `conent.csv` file, contains Dataframe with column `["question", "contexts", "answer"]` (generated from `generate_answer.py`)<br/>
`groundtruth.csv` file, contains Dataframe with column `["groundtruth"]` that is the actual answer of the question in **content.csv** <br/>
<br/>
**Output** ➡️  `eval_customized_metrics_xx-xx-xxxx_xxxx.csv` file, and `eval_customized_metrics_detail_xx-xx-xxxx_xxxx.csv` file <br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_customized_metrics_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "customized_matrics"]` <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"customized_matrics" being the score from 0-10 of the `content.csv`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- **eval_customized_metrics_detail_xx-xx-xxxx_xxxx.csv**: Dataframe with column `["question", "contexts", "answer", "predicted_answer", "answer_relevancy"]`<br/>

**customized_metrics.py**<br/>
To run this function
1. In the `setting.yaml` file, in the `customized_metrics` session
&nbsp;&nbsp;&nbsp;&nbsp;1.1 Store your `content_csv_location` and `content_csv_name` of the **content.csv** file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.2 Store your `ground_truth_csv_location` of the **groundtruth.csv** file<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.3 In the `llm_eval` session, you can choose the model `source` and `name` you want to use for embedding (default model is kornwtp/simcse-model-phayathaibert from huggingface )<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.3 In the `llm_eval` session, you can choose the model `source` and `name` you want to use to evaluate the **content.csv** (default model is llama3.1 70B )<br/>
3. Go to your terminal
4. cd in to the `llm-as-evaluator-main` folder
5. run the following command to evaluated faitfulness<br/>
```
python __customized_matrics/customized_matrics.py
```
<br/>
After run customized_metrics.py, **eval_customized_metrics_xx-xx-xxxx_xxxx.csv** will be generated in the folder specified


## STEP 4: COMPARE

**Input** ➡️ `eval_xxxxxxxxxxx.csv` file, contains results of evaluation run in STEP 2: EVALUATION<br/>
<br/>
**Output** ➡️  `compare_xxxx.txt` file, contain average scores of the metrics you want to compare<br/>

**compare.py**<br/>
To run this function
1. In the `setting.yaml` file, in the `compare` session<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.1 Store your `file_name_list`, which is the list of **eval** file you want to compare<br/>
&nbsp;&nbsp;&nbsp;&nbsp;1.2 in `metric` session, please choose the evaluation result you want to compare form `[faitnfulness, answer_relevancy, customized_matrics]`, The metric should match with the file name
3. Go to your terminal
4. cd in to the `llm-as-evaluator-main` folder
5. run the following command to evaluated faitfulness<br/>
```
python __compare/compare.py
```
<br/>
After run answer_relevancy.py, `compare_xxxx.txt` will be generated in the folder specified
