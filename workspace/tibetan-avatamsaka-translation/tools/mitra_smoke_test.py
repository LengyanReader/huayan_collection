# -*- coding: utf-8 -*-
"""MITRA 冒烟测试：bf16 CPU 加载 + 单段藏→汉试译，计时与内存。
用法: C:\\Users\\data\\miniconda3\\envs\\hy_py312\\python.exe -X utf8 mitra_smoke_test.py
"""
import time, json, io, os, sys

t0 = time.time()
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "buddhist-nlp/mitra-qwen35-translate"
tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
print("tokenizer loaded %.1fs" % (time.time() - t0))
t1 = time.time()
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16, device_map="cpu", local_files_only=True)
print("model loaded %.1fs dtype=%s" % (time.time() - t1, model.dtype))

tib = "བཅོམ་ལྡན་འདས་ཐོག་མ་མངོན་པར་སངས་རྒྱས་པ། སངས་རྒྱས་ཀྱི་ཆོས་ཐམས་ཅད་ཤིན་ཏུ་རྣམ་པར་སངས་རྒྱས་པའི་ཐུགས་མངའ་བ།"
msgs = [{"role": "user", "content":
    "You are an expert translator of classical Buddhist texts. Translate the following Classical Tibetan text into Modern Chinese. "
    "The translation should be fluid and accurate. Provide your answer in Modern Chinese:\n\n" + tib}]
inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_dict=True, return_tensors="pt", enable_thinking=False)
t2 = time.time()
with torch.no_grad():
    out = model.generate(**inputs, max_new_tokens=160, do_sample=False)
gen = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print("gen %.1fs ->" % (time.time() - t2), gen)
io.open(os.path.join(os.path.dirname(__file__), "smoke_result.json"), "w", encoding="utf-8").write(
    json.dumps({"zh": gen, "load_s": round(time.time() - t0, 1), "gen_s": round(time.time() - t2, 1)}, ensure_ascii=False, indent=1))
print("total %.1fs" % (time.time() - t0))
