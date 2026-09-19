LLM
    Large Language Model

RAG
    Retrival Augumented Generation

RAG Arch
    

RAG Evaluation

RAG Matrics
    1) Precision
    2) Recall
    3) Faithfulness
    4) Relevence
    5) Correctness

End to End Application


1) client # connecting to llms

2) collection           # table = evaluation_documents








1) curl http://127.0.0.1:8000/health

2) curl -X POST http://127.0.0.1:8000/index

3) curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is Python?"}'

4) curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is Pandas?"}'


5) curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is NumPy?"}'


6) curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is Matplotlib?"}'

--------------------------------------------------
7) curl -X POST http://127.0.0.1:8000/evaluate \
-H "Content-Type: application/json" \
-d '{"question":"What is Python?"}'


8) curl -X POST http://127.0.0.1:8000/evaluate \
-H "Content-Type: application/json" \
-d '{"question":"What is Pandas?"}'


9) curl -X POST http://127.0.0.1:8000/evaluate \
-H "Content-Type: application/json" \
-d '{"question":"What is NumPy?"}'


10) curl -X POST http://127.0.0.1:8000/evaluate \
-H "Content-Type: application/json" \
-d '{"question":"What is Matplotlib?"}'


11) curl -X POST http://127.0.0.1:8000/evaluate-all

12) curl -X POST http://127.0.0.1:8000/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is Kubernetes?"}'