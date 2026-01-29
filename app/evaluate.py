
# Evaluation Dataset
questions = [ "What was Mrs. Hudson's alibi?", 
             "Who was seen leaving the manor at midnight?", 
             "Did the butler have a motive?" ] 
ground_truths = [ "Mrs. Hudson's alibi is that she was not directly involved in the crime, as indicated by her fear of being accused and her discovering the body. Holmes notes evidence that contradicts her involvement.",
                  "The text does not identify a specific person leaving the manor at midnight. It mentions a 'pale Scotsman' visiting earlier.", 
                  "The text does not mention a butler or a motive for a butler." ]

# Evaluation rows
eval_rows = { "question": [], "answer": [], "contexts": [], "ground_truth": [] }


def test_rag_system():
    return "Still Building"
