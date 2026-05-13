from fastembed import TextEmbedding

_model: TextEmbedding | None = None
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(_MODEL_NAME)
    return _model


def embed(text: str) -> list[float]:
    return next(get_model().embed([text])).tolist()


def embed_batch(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in get_model().embed(texts)]
