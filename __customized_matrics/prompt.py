def prompt_generation(reference, question, written_answer, answer):
    messages = {
        "messages": [
            {
            "content": "You are a careful grader tasked with evaluating the differences between a response from a model and an answer written by a human.",
            "role": "system"
            },
            {
            "content": f"""User question: {question}

Sources that was retrieved from vector database (Could be right or wrong):
{reference}

Model Answer written by human which is always right:
{written_answer}

Response from the model:
{answer}

Model Grading Criteria:

Accuracy of Information (0-4 points):
4 points: The response is perfectly accurate, matching the model answer without any discrepancies.
2-3 points: Minor differences from the model answer are present, but they do not significantly distort the informational content.
0-1 point: Major discrepancies from the model answer, or content not found in the model answer, greatly affecting the response's credibility.

Relevance and Completeness (0-3 points):
3 points: The response completely aligns with the model answer in terms of relevance, addressing the query in full.
1-2 points: The response generally aligns with the model answer but misses some important nuances or aspects.
0 points: Significant deviation from the model answer in terms of relevance or completeness, missing key portions of the query or altering the intended information.

Clarity and Coherence (0-2 points):
2 points: The response maintains the clarity and structure of the model answer, well-structured and coherent.
1 point: Minor deviations in clarity or coherence from the model answer, with some grammatical/style issues or logical inconsistencies.
0 points: Major divergence from the model answer in terms of structure or coherence, difficult to understand or poorly articulated.

Traceability (0-1 point):
1 point: All information in the response can be directly traced to and aligns with the model answer.
0 points: The response introduces conjectures or contains untraceable pieces of information not aligned with the model answer.

Qualitative Feedback:
Compare the model response with the human written response as the ground truth, to grade the model response out of 10.

Response Format:
Score out of 10: []

Response:""",
            "role": "user"
            },
            {
            "content": "Score out of 10: [",
            "role": "assistant"
            },
        ]
    }
    return messages["messages"]