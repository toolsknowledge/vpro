# Adaptive RAG Guide

## Definition

**Adaptive RAG** is a Retrieval-Augmented Generation design in which the system decides, for every user query,
*whether* and *how* to retrieve before answering. A standard (naive) RAG pipeline always retrieves, even for
"Hello". Adaptive RAG first classifies the query and then follows the cheapest strategy that can answer it well.
This reduces cost and latency and avoids forcing irrelevant document context into simple conversations.

## The three routes used in this course

| Route | When it is used | What happens |
|-------|-----------------|--------------|
| DIRECT | Greetings, small talk, general-knowledge questions not tied to the course documents | The LLM answers directly. No vector search is performed and no sources are shown. |
| RETRIEVE | Questions about the course notes or indexed documents | The query is embedded, ChromaDB returns the top-k chunks, a relevance check filters them, and the LLM answers only from the remaining context with citations. |
| CLARIFY | Ambiguous or incomplete questions such as "Explain it" with no earlier topic | The assistant asks a short follow-up question. No retrieval is performed. |

## Query classification

The router is an LLM call with a strict output schema. It receives the question, a short window of conversation
history, and the list of indexed documents, and must return JSON with three fields:

- `route` - one of DIRECT, RETRIEVE, CLARIFY
- `reason` - one sentence explaining the decision (shown to the learner)
- `clarifying_question` - required when the route is CLARIFY

The output is validated with a Pydantic model. If it is malformed, the system uses a documented fallback route
instead of crashing. The router output is treated purely as data: it never executes code or tools.

Conversation history matters. "What about the second one?" is ambiguous on its own, but if the previous answer
listed Hybrid RAG and Advanced RAG, the router can resolve "the second one" to Advanced RAG and retrieve.

## Retrieval relevance checks

Retrieving is not enough - the retrieved chunks must actually be relevant. Each chunk returned by ChromaDB has a
cosine similarity score between the question and the chunk. Chunks below a configurable **relevance threshold**
(0.35 by default in this project) are discarded. If no chunk passes the threshold, the assistant says that the
indexed documents do not contain enough information instead of inventing an answer.

## Example routing scenarios

1. "Hi, how are you?" -> DIRECT. A greeting needs no documents.
2. "What is RAG in simple words?" -> usually DIRECT. It is a general question that the LLM can answer.
3. "Explain Adaptive RAG from the course notes." -> RETRIEVE. The learner explicitly asks for the notes.
4. "What is the difference between Hybrid RAG and Advanced RAG in our documents?" -> RETRIEVE.
5. "Explain it." as the first message -> CLARIFY. There is no topic to explain.
6. "Compare these two." after a message that named two techniques -> RETRIEVE with the references resolved.
7. "What is the capital of France according to our notes?" -> RETRIEVE, but the relevance check finds nothing,
   so the assistant reports that the documents do not cover it.

## Benefits and trade-offs

- Benefit: fewer embedding and vector-search calls, lower latency for simple messages.
- Benefit: clarification prevents confident answers to questions the system did not understand.
- Trade-off: the classifier is an extra LLM call and can misroute borderline questions, so routing decisions
  should be visible to users and the relevance check acts as a safety net.
