# LLM Test Bench

Compare LLM providers (AWS Bedrock/Claude, OpenAI, Google Gemini) on vision tasks with structured output.

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

## Example Output

```
🎉 Test complete!
✅ Successful: 3
❌ Failed: 0
✅ openai: 1250ms
✅ bedrock_claude: 890ms
✅ gemini: 1100ms
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

## Requirements

- Python 3.8+
- API keys for the providers you want to test
- Test images in supported formats (JPG, PNG, GIF, WebP)
