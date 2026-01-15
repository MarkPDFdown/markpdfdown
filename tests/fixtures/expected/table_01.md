# a

# Published as a conference paper at COLM 2024

| Model | COPA | HellaSwag | MMLU | Humaneval | Triviaqa | Lambda | Squad2.0 | GSM8k | C-Eval | CMMLU |
|-------|------|-----------|------|-----------|----------|---------|----------|--------|--------|--------|
| Qwen1.5-1.8B | 53.0 | 55.99 | 47.06 | 18.9 | 31.15 | 56.39 | 30.06 | 35.1 | 59.38 | 57.1 |
| TinyLlama-1.1B | 51.0 | 54.47 | 25.89 | 8.54 | 31.27 | 59.71 | 20.85 | 5.36 | 26.16 | 25.04 |
| StableIm-3b-4e11 | 61.0 | 69.08 | 45.42 | 15.85 | 50.54 | 70.38 | 36.44 | 10.92 | 31.71 | 31.48 |
| Gemma-2b | 64.0 | 64.96 | 41.84 | 9.15 | 46.42 | 63.38 | 6.66 | 22.14 | 31.25 | 31.11 |
| Phi-2 | 72.0 | 67.74 | 57.62 | 40.24 | 41.04 | 62.7 | 34.81 | 61.41 | 31.53 | 32.19 |
| CT-LLM(Ours) | 59.0 | 50.37 | 37.11 | 9.15 | 21.03 | 56.24 | 18.87 | 8.87 | 36.78 | 36.4 |

Table 2: Performance comparison of CT-LLM and other base models of the similar scale on benchmark. The best result are in blue, the second-best results are underline, and the third-best results are in fbox. The evaluation metric employed for 'HumanEval' is 'pass@1', a standard maintained consistently throughout the text.

Training Process and Comparative Analysis   The training progress reveals a consistent trend of improvement across various datasets, with particular strides seen in language understanding, reasoning, and domain-specific knowledge.  Notably, datasets such as HellaSwag, PiQA, and ARC show marked improvements, indicative of enhanced reasoning capabilities. The model shows notable progress in specialized fields such as mathematics (GSM8K and TheoremQA) and science (ARC-c and ARC-e), emphasizing its increasing ability to understand and produce content specific to these domains. The evaluation results of the intermediate checkpoints during our pre-training process are shown in Table.4.

Comparing our model's performance on both English and Chinese benchmarks with other models reveals a notably smaller gap in performance across multi-disciplinary datasets such as MMLU and CMMLU, as shown in Table 2.  While other models exhibit significant disparities, particularly in language understanding and reasoning benchmarks, our model maintains a consistent performance, suggesting a balanced capability across diverse domains. This contrasts with other models that show pronounced variability, such as in the HellaSwag dataset, where our model clearly rivals or outperforms alternatives like MiniCPM (min, 2024) and Phi-2, showcasing superior or competitive reasoning abilities. Similarly, in domain-specific evaluations (C-Eval and CMMLU), our model demonstrates commendable performance, outpacing models like TinyLlama-1.1B and Bloom-1.7B in comprehending and generating content that requires a nuanced understanding of cultural and domain-specific contexts. This balanced proficiency underscores the model's versatility and adaptability, positioning it as a strong contender in the landscape of AI language models, with a capacity for both broad applicability and deep, domain-specific knowledge.

We also compared the performance of our model, which was fine-tuned using a 2:1 ratio of Chinese to English data (SFT), with other models on common benchmarks and Chinese benchmarks, as shown in Table.3. We found that our model's capability in Chinese remains particularly strong.  The data ratio used for this SFT model is consistent with that of pretraining. We found its overall performance to be the best. The performance of models trained with other ratios can be found in the Appendix.E.2.

| Model | COPA | HellaSwag | MMLU | Humaneval | Triviaqa | Lambda | Squad2.0 | GSM8k | C-Eval | CMMLU |
|-------|------|-----------|------|-----------|----------|---------|----------|--------|--------|--------|
| MiniCPM-2B-sft-fp32 | 66.0 | 65.88 | 53.87 | 45.12 | 36.24 | 60.62 | 40.52 | 55.8 | 49.14 | 51.0 |
| Gemma-2b-it | 60.0 | 56.85 | 37.71 | 0.0 | 29.0 | 55.91 | 18.46 | 15.69 | 32.3 | 33.07 |
| TinyLlama-1.1B-Chat-v1.0 | 48.0 | 56.44 | 25.38 | 4.88 | 15.21 | 61.09 | 12.89 | 3.72 | 24.61 | 24.92 |
| Bloom-1.7B | 57.0 | 44.42 | 27.33 | 1.83 | 24.31 | 48.56 | 14.49 | 1.54 | 22.51 | 24.25 |
| Deepseek-Coder-1.3B-instruct | 51.0 | 37.0 | 28.55 | 43.29 | 10.85 | 35.32 | 28.85 | 8.79 | 28.33 | 27.75 |
| Qwen1.5-1.8B-Chat | 57.0 | 55.75 | 45.86 | 6.71 | 24.31 | 48.83 | 47.95 | 28.73 | 56.84 | 54.11 |
| StableIm-zephyr-3B | 64.0 | 67.94 | 46.15 | 24.39 | 33.48 | 57.46 | 21.19 | 57.01 | 29.5 | 32.11 |
| CT-LLM-SFT(Ours) | 60.0 | 52.93 | 39.95 | 10.37 | 22.88 | 51.93 | 35.18 | 19.18 | 41.54 | 41.48 |
| CT-LLM-SFT-DPO(Ours) | 61.0 | 53.38 | 39.82 | 7.93 | 23.64 | 51.47 | 31.36 | 18.5 | 41.18 | 42.01 |

Table 3: Performance of aligned models with a scale of around 2B on benchmark. The best result are in blue, the second-best are underline, and the third-best are in fbox.

Safety Evaluation   We also evaluate the safety score of CT-LLM-SFT-DPO compared with baselines such as MiniCPM-2B-sft-fp, Bloom-1.7B, and StableIm-zephyr-3B, etc on evalues responsibility benchmark (Xu et al., 2023). The evaluation consists of two parts: multiple-choice and question-answering. The multiple-choice part includes 1,712 input examples, each comprising a human query and two candidate responses. The evaluated models are

7
