import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit.processor import IndicProcessor


class EnglishToIndicTranslator:

    def __init__(self):
        self.model_name = "ai4bharat/indictrans2-en-indic-dist-200M"

        print("Loading IndicTrans2 English → Indic model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model.eval()

        self.processor = IndicProcessor(inference=True)

        print("Model loaded successfully!")

    def translate(self, text, target_language):

        source_language = "eng_Latn"

        # Preprocess the English input
        batch = self.processor.preprocess_batch(
            [text],
            src_lang=source_language,
            tgt_lang=target_language
        )

        # Tokenize
        inputs = self.tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            return_attention_mask=True
        )

        # Generate translation
        with torch.no_grad():
            generated_tokens = self.model.generate(
                **inputs,
                use_cache=True,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1
            )

        # Convert tokens to text
        generated_tokens = self.tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True
        )

        # Postprocess
        translations = self.processor.postprocess_batch(
            generated_tokens,
            lang=target_language
        )

        return translations[0]


if __name__ == "__main__":

    translator = EnglishToIndicTranslator()

    text = "Is it going to rain in Hyderabad tomorrow?"

    result = translator.translate(
        text,
        "tel_Telu"
    )

    print("\nEnglish:")
    print(text)

    print("\nTelugu:")
    print(result)
