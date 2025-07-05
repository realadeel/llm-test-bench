# LLM Test Bench - AI Model Comparison Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Compare LLM providers (AWS Bedrock/Claude, OpenAI GPT-4 Vision, Google Gemini) on vision tasks with structured output. Perfect for evaluating AI models for production use, Lambda deployments, and cost optimization.

## 🚀 Features

- **Multi-provider support**: AWS Bedrock, OpenAI, Google Gemini
- **Vision + structured output**: Test image analysis with JSON schemas  
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

4. **Configure tests in `config.yaml`:**
```yaml
providers:
  - name: "openai"
    model: "gpt-4-vision-preview"
  - name: "bedrock_claude"
    model: "anthropic.claude-3-sonnet-20240229-v1:0"

test_cases:
  - name: "Image Analysis"
    prompt: "Describe what you see in this image."
    image_path: "test_images/sample.jpg"
    max_tokens: 2000
    temperature: 0.7
```

5. **Run tests:**
```bash
python llm_test_bench.py
```

Results are saved to `results/test_results_TIMESTAMP.json`.

## Features

- **Multi-provider support**: AWS Bedrock, OpenAI, Google Gemini
- **Vision + structured output**: Test image analysis with JSON schemas
- **Production-ready**: Async operations, error handling, rate limiting
- **Lambda-compatible**: Designed for serverless deployment

## Configuration

Edit `config.yaml` to:
- Choose which providers/models to test
- Define test cases with custom prompts
- Set image paths and parameters
- Configure structured output schemas

API keys are loaded from `.env` file (never committed).

## 📈 Example Output

```
🎉 Test complete!
✅ Successful: 3
❌ Failed: 0
✅ openai: 1250ms (1,240 tokens, $0.048)
✅ bedrock_claude: 890ms (980 tokens, $0.012)
✅ gemini: 1100ms (1,150 tokens, $0.008)
```

## 🔧 Advanced Configuration

### Structured Output with JSON Schema

```yaml
test_cases:
  - name: "Object Detection"
    prompt: "Identify objects in this image with locations and confidence scores."
    image_path: "test_images/sample.jpg"
    schema:
      type: "object"
      properties:
        objects:
          type: "array"
          items:
            type: "object"
            properties:
              name: {type: "string"}
              confidence: {type: "number"}
              bbox: {type: "array"}
```

### Multiple Test Cases

```yaml
test_cases:
  - name: "Document Analysis"
    prompt: "Extract text and structure from this document."
    image_path: "test_images/invoice.png"
  - name: "Medical Image Analysis"  
    prompt: "Analyze this medical scan for abnormalities."
    image_path: "test_images/xray.jpg"
```

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

`llm-comparison` `ai-benchmark` `openai-api` `claude-api` `gemini-api` `vision-ai` `multimodal-ai` `api-testing` `cost-optimization` `lambda-deployment` `serverless-ai` `production-ai` `ai-evaluation` `model-comparison` `llm-benchmark`

---

**Star ⭐ this repo if it helps you choose the right AI provider!**
