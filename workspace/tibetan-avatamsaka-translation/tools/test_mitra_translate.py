import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Use hy_py312 environment
model_name = "buddhist-nlp/mitra-qwen35-translate"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # CPU
    device_map="cpu"
)

# Sample from Derge vol 035 - first few lines of actual sutra text (skip titles/colophons)
# Take a short passage
tibetan_text = """།འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན། བཅོམ་ལྡན་འདས་ཐོག་མ་མངོན་པར་སངས་རྒྱས་པ། སངས་རྒྱས་ཀྱི་ཆོས་ཐམས་ཅད་ཤིན་ཏུ་རྣམ་པར་སངས་རྒྱས་པའི་ཐུགས་མངའ་བ།"""

# Translate to Modern Chinese
messages = [{"role": "user", "content": f"You are an expert translator of classical Buddhist texts. Translate the following Classical Tibetan text into Modern Chinese. The translation should be fluid and accurate. Provide your answer in Modern Chinese:\n\n{tibetan_text}"}]

inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_dict=True, return_tensors="pt", enable_thinking=False).to(model.device)
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=512, temperature=0.1, do_sample=False)
result = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print("=== ZH TRANSLATION ===")
print(result)
print("\n\n=== EN TRANSLATION ===")

# Translate to English
messages_en = [{"role": "user", "content": f"You are an expert translator of classical Buddhist texts. Translate the following Classical Tibetan text into English. The translation should be fluid and accurate. Provide your answer in English:\n\n{tibetan_text}"}]
inputs_en = tokenizer.apply_chat_template(messages_en, add_generation_prompt=True, return_dict=True, return_tensors="pt", enable_thinking=False).to(model.device)
with torch.no_grad():
    out_en = model.generate(**inputs_en, max_new_tokens=512, temperature=0.1, do_sample=False)
result_en = tokenizer.decode(out_en[0][inputs_en["input_ids"].shape[1]:], skip_special_tokens=True)
print(result_en)
