from types import SimpleNamespace

import httpx
import openai
import pytest

from backend.embeddings import OpenAIEmbedder
from backend.errors import EmbeddingError


def resp(n, start=0):
    return SimpleNamespace(data=[SimpleNamespace(index=i, embedding=[float(i)] * 3) for i in range(n)])


class Client:
    def __init__(self, behaviours):
        self.behaviours, self.calls = list(behaviours), 0
        self.embeddings = SimpleNamespace(create=self._create)

    def _create(self, model, input):
        self.calls += 1
        b = self.behaviours.pop(0)
        if isinstance(b, Exception):
            raise b
        return resp(len(input))


def err(cls, status=429, body=None):
    r = httpx.Response(status, request=httpx.Request("POST", "https://x"))
    return cls("msg", response=r, body=body)


def test_batches_and_order():
    c = Client([None, None])
    out = OpenAIEmbedder(c, "m", batch_size=2).embed_texts(["a", "b", "c"])
    assert len(out) == 3 and c.calls == 2


def test_transient_error_is_retried_with_backoff():
    sleeps = []
    c = Client([err(openai.RateLimitError), None])
    e = OpenAIEmbedder(c, "m", sleep=sleeps.append)
    assert len(e.embed_texts(["a"])) == 1 and e.retries == 1 and sleeps == [1.0]


def test_retries_are_bounded():
    c = Client([err(openai.RateLimitError)] * 5)
    with pytest.raises(EmbeddingError, match="rate limit"):
        OpenAIEmbedder(c, "m", max_attempts=3, sleep=lambda s: None).embed_texts(["a"])
    assert c.calls == 3


def test_quota_and_auth_not_retried():
    c = Client([err(openai.RateLimitError, body={"code": "insufficient_quota"})])
    with pytest.raises(EmbeddingError, match="quota"):
        OpenAIEmbedder(c, "m", sleep=lambda s: None).embed_texts(["a"])
    assert c.calls == 1
    c = Client([err(openai.AuthenticationError, 401)])
    with pytest.raises(EmbeddingError, match="API key"):
        OpenAIEmbedder(c, "m").embed_texts(["a"])
    assert c.calls == 1


def test_empty_text_rejected():
    with pytest.raises(EmbeddingError):
        OpenAIEmbedder(Client([]), "m").embed_texts([" "])
    with pytest.raises(EmbeddingError):
        OpenAIEmbedder(Client([]), "m").embed_query("")
