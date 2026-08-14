def process_query(question):
    question = question.strip()
    question = " ".join(
        question.split()
    )
    return question