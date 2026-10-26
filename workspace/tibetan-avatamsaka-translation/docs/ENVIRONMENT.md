# 测试环境记录

## Conda 环境（默认）
- **环境名**：`hy_py312`
- **路径**：`C:\Users\data\miniconda3\envs\hy_py312`
- **Python**：3.12（推断）
- **设为默认**：是（后续藏译测试统一使用此环境）

## 当前状态（2025-10-25）
```bash
C:\Users\data\miniconda3\envs\hy_py312\python.exe -c "import torch,transformers; print(torch.__version__); print(torch.cuda.is_available())"
# torch 2.13.0+cpu
# cuda: False
```

- **PyTorch**: 2.13.0+cpu（无 CUDA）
- **Transformers**: 已安装
- **其他**: 需安装 `accelerate`, `sentencepiece`, `safetensors`, `huggingface_hub`（如缺失）

## 使用方式
```bash
# 激活/直接调用
C:\Users\data\miniconda3\envs\hy_py312\python.exe <script.py>
# 或
conda activate hy_py312  # 若 shell 已初始化 conda
```

## 注意
- 当前为 CPU 环境，`mitra-qwen35-translate`（9B）在纯 CPU 上推理会较慢，但仍可用于小规模测试（1-2 段）验证流程。
- 如有 GPU 可用，后续可切换到 CUDA 版本的 PyTorch 以提升速度。
