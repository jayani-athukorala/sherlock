# Imports
from datasets import Dataset
import os
from ragas import evaluate
from ragas.metrics import faithfullness, answer_correctness
from app.rag import find_context, generate_answer

# Evaluation Dataset
questions = [ "What was Mrs. Hudson's alibi?", 
             "Who was seen leaving the manor at midnight?", 
             "Did the butler have a motive?" ] 
ground_truths = [ "Mrs. Hudson's alibi is that she was not directly involved in the crime, as indicated by her fear of being accused and her discovering the body. Holmes notes evidence that contradicts her involvement.",
                  "The text does not identify a specific person leaving the manor at midnight. It mentions a 'pale Scotsman' visiting earlier.", 
                  "The text does not mention a butler or a motive for a butler." ]

# Evaluation rows
eval_rows = { "question": [], "answer": [], "contexts": [], "ground_truth": [] }


def generate_sample():
    # Clear previous results 
    eval_rows["question"] = [] 
    eval_rows["answer"] = [] 
    eval_rows["contexts"] = [] 
    eval_rows["ground_truth"] = [] 
    
    for question, ground_truth in zip(questions, ground_truths):
        # Retrieve context 
        context = find_context(question) 
        
              
        # Generate answer 
        answer = generate_answer(question) 
        
        # Append to evaluation rows 
        eval_rows["question"].append(question) 
        eval_rows["answer"].append(answer) 
        eval_rows["contexts"].append(context)
        eval_rows["ground_truth"].append(ground_truth) 
        
    return eval_rows

def test_rag_system():
    
    eval_rows = generate_sample()
    dataset = Dataset.from_dict(eval_rows)
    results = evaluate(dataset, metrics=[faithfullness, answer_correctness])
    return results
