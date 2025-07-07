# 📊 LLM Test Bench Documentation

Welcome to the comprehensive documentation for LLM Test Bench!

## 🚀 Quick Navigation

- **[Configuration Guide](#-configuration-guide)** - Set up your tests and providers
- **[Multi-Tool Testing](#-multi-tool-testing)** - Let AI choose analysis methods
- **[Structured Output](#-structured-output)** - Traditional single-schema testing
- **[Examples](#-examples)** - Real-world usage examples
- **[API Reference](#-api-reference)** - Detailed configuration options

## 🌟 What is LLM Test Bench?

LLM Test Bench is a production-ready tool for comparing Large Language Model providers on vision tasks with structured output. It helps you:

- **Compare providers**: OpenAI, AWS Bedrock (multiple models), Google Gemini
- **Vision Model Support**: Test Llama 4, Claude, Pixtral, GPT-4V, and Gemini vision models
- **Test structured output**: JSON schemas, multi-tool selection, function calling
- **Measure performance**: Latency, accuracy, token usage
- **Deploy confidently**: Production-ready for Lambda and serverless environments

## 📊 Example Results

```
🎉 Test complete!
📊 Test Cases: 1
✅ Successful Provider Calls: 3
❌ Failed Provider Calls: 0

📝 Production-Optimized Multi-Tool Analysis:
  ✅ bedrock_llama_4_maverick: 1101ms
  ✅ bedrock_llama_4_scout: 1307ms
  ✅ bedrock_pixtral: 9240ms

📊 Results saved to results/test_results_20250707_015405.json
```

### Optimized JSON Structure

Results are organized by test case with efficient storage:

```json
[
  {
    "name": "Production-Optimized Multi-Tool Analysis",
    "prompt": "You are a professional appraiser...",
    "image_path": "test_images/Radioheadokcomputer.png",
    "max_tokens": 2000,
    "temperature": 0.1,
    "provider_results": [
      {
        "provider": "bedrock_llama_4_maverick",
        "model": "us.meta.llama4-maverick-17b-instruct-v1:0",
        "response": "{...}",
        "latency_ms": 1101.5,
        "timestamp": "2025-07-07T01:53:52.253486",
        "error": null,
        "tokens_used": 107
      }
    ],
    "tools": [...]
  }
]
```

**Benefits:**
- 💾 **Smaller files** (no prompt duplication)
- 📁 **Better organization** (results grouped logically)
- 🔍 **Easier analysis** (compare providers within each test case)
- ⚙️ **Full compatibility** (all original data preserved)

---

**Ready to start benchmarking?** Check out the example configuration in `config.yaml.example`! 🚀
