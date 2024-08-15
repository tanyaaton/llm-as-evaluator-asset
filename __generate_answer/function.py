from milvus import default_server, debug_server
from pymilvus import connections, utility, Collection,CollectionSchema, FieldSchema,DataType
import logging
import datetime
import ast
from __generate_answer.prompt import generate_answer_prompt_en
from prompt_template import get_prompt_template

now = datetime.datetime.now()
formatted_datetime = now.strftime("%d-%m-%Y_%H%M")
logging.basicConfig(filename=f'log/generate_answer{formatted_datetime}.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
col_name = 'a'+now.strftime("%d_%m_%Y_%H%M")

def create_milvus_db(collection_name):
    item_id    = FieldSchema( name="id",         dtype=DataType.INT64,    is_primary=True, auto_id=True )
    text       = FieldSchema( name="text",       dtype=DataType.VARCHAR,  max_length= 50000             )
    embeddings = FieldSchema( name="embeddings", dtype=DataType.FLOAT_VECTOR,    dim=768                )
    schema     = CollectionSchema( fields=[item_id, text, embeddings], description="Inserted policy from user", enable_dynamic_field=True )
    collection = Collection( name=collection_name, schema=schema, using='default' )
    return collection


def drop_milvus_collection():
    utility.drop_collection(col_name)
    print('dropped milvus collection')


def split_text_with_overlap(text, chunk_size, overlap_size):
    chunks = []
    start_index = 0

    while start_index < len(text):
        end_index = start_index + chunk_size
        chunk = text[start_index:end_index]
        chunks.append(chunk)
        start_index += (chunk_size - overlap_size)

    return chunks

def embedding_data(chunks, model_embedding):
    collection_leavepdf = create_milvus_db(col_name)
    if str(type(model_embedding)) == "<class 'sentence_transformers.SentenceTransformer.SentenceTransformer'>":
        vector  = model_embedding.encode(chunks)
        collection_leavepdf.insert([chunks,vector.tolist()])
    elif str(type(model_embedding)) == "<class 'langchain_ibm.embeddings.WatsonxEmbeddings'>":
        vector  = model_embedding.embed_documents(chunks)
        collection_leavepdf.insert([chunks,vector])
    else:
        raise ValueError(f"Invalid model type: embedding_model is not WatsonxEmbeddings or SentenceTransformer model.")
    collection_leavepdf.create_index(field_name="embeddings",\
                                index_params={"metric_type":"IP","index_type":"IVF_FLAT","params":{"nlist":16384}})
    return collection_leavepdf

def find_answer_doc_from_q_df(question_df, collection, model_embedding):
    question_list = question_df['question'].tolist()    # embedding question
    if str(type(model_embedding)) == "<class 'sentence_transformers.SentenceTransformer.SentenceTransformer'>":
        embedded_question_vector  = model_embedding.encode(question_list)
    elif str(type(model_embedding)) == "<class 'langchain_ibm.embeddings.WatsonxEmbeddings'>":
        embedded_question_vector  = model_embedding.embed_documents(question_list)
    else:
        raise ValueError(f"Invalid model type: embedding_model is not WatsonxEmbeddings or SentenceTransformer model.")
    collection.load()           # query data from collection
    hits = collection.search(data=embedded_question_vector, anns_field="embeddings", param={"metric":"IP","offset":0},
                    output_fields=["text"], limit=5)
    return hits

def generate_doc(question_df, hits):
    for i in question_df.index:
        doc_combine = ''
        for ii in range(len(hits[0])):
            question_df.loc[i,f"doc_{ii}"]  = hits[i][ii].text
            
            doc_combine += hits[i][ii].text + ', '
        question_df.loc[i,'contexts'] = doc_combine


def find_response(model_llm, content_df):
    for i in content_df.index:
        print(i)
        massage = generate_answer_prompt_en(content_df["question"][i], content_df["contexts"][i])
        prompt = get_prompt_template(model_llm, massage)
        answer = model_llm.generate_text(prompt)
        print(answer)
        content_df.loc[i,"answer"]= answer


def find_response_openai(client, model_id, content_df):
    for i in content_df.index:
        print(i)
        massage = generate_answer_prompt_en(content_df["question"][i], content_df["contexts"][i])
        response = client.chat.completions.create(
            model= model_id,
            messages=massage,
            temperature=0, #for greedy: temprature=0, top_p=1
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].message.content
        content_df.loc[i,"answer"]= answer

def find_response_sentence(model_llm, content_df):
    for i in content_df.index:
        print(i)
        massage = generate_answer_prompt_en(content_df["question"][i], content_df["contexts"][i])
        prompt = get_prompt_template(model_llm, massage)
        answer = model_llm.generate(prompt)
        print(answer)
        print(answer[:-2])
        content_df.loc[i,"answer"]= answer[:-2]