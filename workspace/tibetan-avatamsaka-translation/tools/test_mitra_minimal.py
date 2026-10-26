import sys
sys.stdout.reconfigure(encoding='utf-8')

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print("START", flush=True)
model_name = "buddhist-nlp/mitra-qwen35-translate"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("TOKENIZER_LOADED", flush=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    print("MODEL_LOADED", flush=True)
    
    tibetan_text = "།འདི་སྐད་བདག་གིས་ཐོས་པའི་དུས་གཅིག་ན།"
    messages = [{"role": "user", "content": f"Translate the following Classical Tibetan text into Modern Chinese. Provide your answer in Modern Chinese:\n\n{tibetan_text}"}]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_dict=True, return_tensors="pt", enable_thinking=False).to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=32, temperature=0.1, do_sample=False)
    result = tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    print("RESULT:" + result, flush=True)
except Exception as e:
    print("ERR:" + str(e), flush=True)
    import traceback
    traceback.print_exc()
