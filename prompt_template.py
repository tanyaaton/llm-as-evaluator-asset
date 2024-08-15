
import logging

def llama3_prompt_template(messages):
    current_prompt = ""
    for i in range(len(messages)):
        message = messages[i]
        if message["role"] == "system":
            pre_text = "<|eot_id|><|begin_of_text|><|start_header_id|>system<|end_header_id|>"
        elif message["role"] == "user":
            pre_text = "<|eot_id|><|begin_of_text|><|start_header_id|>user<|end_header_id|>"
        elif message["role"] == "assistant":
            pre_text = "<|eot_id|><|begin_of_text|><|start_header_id|>assistant<|end_header_id|>"
        current_prompt += pre_text + message["content"]
    print(current_prompt)
    return current_prompt

def mixtral_prompt_template(messages):
    current_prompt = ""
    for i in range(len(messages)):
        message = messages[i]
        post_text = ''
        if message["role"] == "system":
            pre_text = "<s>[INST]"
        elif message["role"] == "user":
            pre_text = ""
            post_text = "[/INST]"
        current_prompt += pre_text+ message["content"] + post_text
    print(current_prompt)
    return current_prompt

def openai_prompt_template(message):
    return message

#return prompt
def get_prompt_template(model_llm, messages):
    model_id = model_llm.model_id
    if model_id[:10] == 'meta-llama':
        prompt = llama3_prompt_template(messages)
    
    elif model_id == 'mistralai/mixtral-8x7b-instruct-v01'\
    or model_id =='mistralai/mistral-large':
        prompt = mixtral_prompt_template(messages)
    
    return prompt