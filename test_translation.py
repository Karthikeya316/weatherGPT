import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor

MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"

src_lang = "tel_Telu"
tgt_lang = "eng_Latn"

text = "రేపు హైదరాబాద్‌లో వర్షం పడుతుందా?"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

print("Loading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

model.eval()

print("Model loaded successfully!")

ip = IndicProcessor(inference=True)

batch = ip.preprocess_batch(
    [text],
    src_lang=src_lang,
    tgt_lang=tgt_lang
)

inputs = tokenizer(
    batch,
    truncation=True,
    padding="longest",
    return_tensors="pt",
    return_attention_mask=True,
)

with torch.no_grad():
    generated_tokens = model.generate(
        **inputs,
        use_cache=True,
        min_length=0,
        max_length=256,
        num_beams=5,
        num_return_sequences=1,
    )

generated_tokens = tokenizer.batch_decode(
    generated_tokens,
    skip_special_tokens=True,
)

translations = ip.postprocess_batch(
    generated_tokens,
    lang=tgt_lang
)

print("\nOriginal:")
print(text)

print("\nTranslation:")
print(translations[0])
