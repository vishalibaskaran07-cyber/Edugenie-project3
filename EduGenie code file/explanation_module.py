from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

_tokenizer = None
_model = None


def _load_model():
    """Load the tokenizer/model once and cache them (fixes re-loading on every call)."""
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        _model.eval()
    return _tokenizer, _model


def explain_topic(topic: str) -> str:
    try:
        tokenizer, model = _load_model()
        input_text = (
            f"Explain the concept of '{topic}' in a simple and clear way "
            "for a school student."
        )
        # include attention_mask (was missing before, which can cause
        # incorrect generation for padded/short inputs)
        inputs = tokenizer(input_text, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True,
            )

        explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return explanation
    except Exception as e:
        return f"Error in Explanation: {e}"
