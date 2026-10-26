import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print("Loading...")
model_name = "buddhist-nlp/mitra-qwen35-translate"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="cpu",
    low_cpu_mem_usage=True
)
print("Loaded")

tibetan_text = """།འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན།"""

messages = [{"role": "user", "content": f"You are an expert translator of classical Buddhist texts. Translate the following Classical Tibetan text into Modern Chinese. Provide your answer in Modern Chinese:\n\n{tibetan_text}"}]

inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_dict=True, return_tensors="pt", enable_thinking=False).to(model.device)
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=64, temperature=0.1, do_sample=False)
result = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(result)
