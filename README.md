# LLM Test Bench - AI Model Comparison Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Compare LLM providers (AWS Bedrock/Claude, OpenAI GPT-4, Google Gemini) on vision tasks with structured output. Perfect for evaluating AI models for production use, Lambda deployments, and cost optimization.

## 🚀 Features

- **Multi-provider support**: AWS Bedrock, OpenAI, Google Gemini
- **Modern structured output**: Uses each provider's latest JSON schema methods  
- **Production-ready**: Async operations, error handling, rate limiting
- **Lambda-compatible**: Designed for serverless deployment
- **Cost tracking**: Monitor token usage and API costs
- **Benchmark metrics**: Latency, accuracy, and reliability comparison

## 📊 Use Cases

- **API evaluation**: Choose the best LLM provider for your use case
- **Cost analysis**: Optimize AI spending with usage metrics
- **A/B testing**: Compare prompts, models, and parameters
- **Production deployment**: Production-ready for serverless applications
- **Research**: Academic and commercial AI model evaluation

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API keys in `.env`:**
```bash
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
```

3. **Add test images to `test_images/`**

4. **Configure tests:**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your test cases and image paths
```

5. **Run tests:**
```bash
python llm_test_bench.py
```

Results are saved to `results/test_results_TIMESTAMP.json`.

## 🎯 Modern Structured Output

Each provider uses their most advanced structured output method:

- **OpenAI**: `json_schema` with strict validation
- **Claude**: Tool use with input schemas 
- **Gemini**: `responseSchema` in generation config

Example configuration:

```yaml
test_cases:
  - name: "Object Detection"
    prompt: "Identify all objects in this image with locations and confidence scores."
    image_path: "test_images/photo.jpg"
    schema:
      type: "object"
      properties:
        objects:
          type: "array"
          items:
            properties:
              name: {type: "string"}
              confidence: {type: "number", minimum: 0.0, maximum: 1.0}
              location:
                type: "object"
                properties:
                  x: {type: "number"}
                  y: {type: "number"}
            required: ["name", "confidence"]
      required: ["objects"]
      additionalProperties: false
```

## 📈 Example Output

```
🎉 Test complete!
✅ Successful: 3
❌ Failed: 0
✅ openai: 1,250ms (1,240 tokens)
✅ bedrock_claude: 890ms (980 tokens)  
✅ gemini: 1,100ms (1,150 tokens)
```

## 🔧 Configuration

Edit `config.yaml` to:
- Choose providers and models to test
- Define test cases with custom prompts
- Set image paths and parameters
- Configure JSON schemas for structured output

API keys are loaded from `.env` file (never committed).

## 🌟 Latest Models Supported

- **OpenAI**: `gpt-4.1-nano-2025-04-14`
- **Bedrock Claude**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Gemini**: `gemini-2.0-flash-lite`

## Use Cases

- **API evaluation**: Compare providers for your specific use case
- **Cost analysis**: Track token usage and latency
- **A/B testing**: Test different prompts and parameters
- **Lambda deployment**: Production-ready for serverless apps

## License

MIT License - see [LICENSE](LICENSE) file.

## Contributing

Pull requests welcome! Please:
1. Keep it simple
2. Add tests for new features
3. Update documentation

## 🔍 Keywords

`llm-comparison` `ai-benchmark` `openai-api` `claude-api` `gemini-api` `vision-ai` `multimodal-ai` `api-testing` `cost-optimization` `lambda-deployment` `serverless-ai` `production-ai` `ai-evaluation` `model-comparison` `llm-benchmark` `structured-output` `json-schema`

---

**Star ⭐ this repo if it helps you choose the right AI provider!**
