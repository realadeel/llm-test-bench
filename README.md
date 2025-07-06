# 🚀 LLM Test Bench

An open source benchmarking tool for comparing Large Language Model providers during prompt engineering. Test OpenAI, AWS Bedrock, and Google Gemini side-by-side to optimize performance, cost, and accuracy across any content type.

## ✨ Features

- **Multi-Provider Support**: Compare OpenAI, AWS Bedrock, and Google Gemini
- **Flexible Input**: Test with text prompts, images, documents, or any content type
- **Structured Output Testing**: Compare how well each provider follows your JSON schemas
- **Multi-Tool Testing**: Let AI choose the best analysis method from multiple options
- **Modern API Integration**: Uses each provider's latest structured output methods:
  - OpenAI: `json_schema` and function calling
  - Claude: Tool use with structured schemas  
  - Gemini: `responseSchema` with union types
- **Raw Response Comparison**: See authentic output formatting from each provider
- **Production Ready**: Async operations, error handling, rate limiting
- **Cost Tracking**: Monitor token usage and latency across providers
- **Configurable**: YAML-based test configuration with environment variables

## 🎯 Use Cases

- **Prompt Engineering**: Compare how different providers handle your prompts
- **Schema Validation**: Test which provider best follows your structured output requirements
- **Multi-Tool Selection**: Benchmark AI's ability to choose appropriate analysis methods
- **Cost Optimization**: Find the most cost-effective provider for your specific use case
- **Performance Testing**: Measure latency and reliability across providers

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/realadeel/llm-test-bench.git
cd llm-test-bench
pip install -r requirements.txt
```

### 2. Set Up API Keys
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required keys:
- `OPENAI_API_KEY` - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` - Get from [AWS Console](https://console.aws.amazon.com/iam/)
- `GEMINI_API_KEY` - Get from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key)

### 3. Configure Your Test
Copy and customize the config:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your test cases
```

### 4. Add Test Content
```bash
# Add your test images/documents to test_images/
cp your_content.jpg test_images/
```

### 5. Run Benchmark
```bash
python llm_test_bench.py
```

## 📊 Example Output

```
🎉 Test complete!
✅ Successful: 3
❌ Failed: 0
✅ bedrock_claude: 2,081ms (179 tokens)
✅ openai: 1,417ms (539 tokens)  
✅ gemini: 2,025ms (496 tokens)

🏆 Fastest: OpenAI (1,417ms)
💰 Most efficient: Bedrock Claude (179 tokens)

📊 Results saved to results/test_results_TIMESTAMP.json
```

## 🔧 Configuration

### Multi-Tool Testing
Let the AI choose the best analysis method:

```yaml
test_cases:
  - name: "Multi-Tool Analysis"
    prompt: "Analyze this image and choose the appropriate tool..."
    image_path: "test_images/album_cover.jpg"
    tools:
      - name: "analyze_vinyl_record"
        description: "For vinyl records and LPs"
        schema:
          type: "object"
          properties:
            title: {type: "string"}
            artist: {type: "string"}
            genre: {type: "string"}
          required: ["title", "artist"]
      
      - name: "analyze_book"
        description: "For books and publications"
        schema:
          type: "object"
          properties:
            title: {type: "string"}
            author: {type: "string"}
            publisher: {type: "string"}
          required: ["title", "author"]
```

### Single Schema Testing
Traditional structured output testing:

```yaml
test_cases:
  - name: "Object Detection"
    prompt: "List all objects in this image"
    image_path: "test_images/scene.jpg"
    schema:
      type: "object"
      properties:
        objects:
          type: "array"
          items:
            properties:
              name: {type: "string"}
              confidence: {type: "number"}
        total_count: {type: "integer"}
      required: ["objects", "total_count"]
```

## 📁 Project Structure

```
llm-test-bench/
├── llm_test_bench.py      # Main benchmarking engine
├── config.yaml           # Your test configuration
├── config.yaml.example   # Example configuration
├── test_images/          # Your test images
├── results/              # Benchmark results (JSON)
├── docs/                 # Documentation website
└── requirements.txt      # Dependencies
```

## 🎛️ Advanced Configuration

### Provider Settings
```yaml
providers:
  - name: "bedrock_claude"
    model: "anthropic.claude-3-haiku-20240307-v1:0"
  - name: "openai" 
    model: "gpt-4o-mini"
  - name: "gemini"
    model: "gemini-1.5-flash"

# Rate limiting
delay_between_calls: 1      # seconds between API calls
delay_between_test_cases: 2 # seconds between test cases
```

### Test Parameters
```yaml
test_cases:
  - name: "Custom Test"
    prompt: "Your analysis prompt..."
    image_path: "test_images/image.jpg"
    max_tokens: 2000
    temperature: 0.7
    # ... schema or tools
```

## 🔍 How It Works

1. **Loads Configuration**: Reads your test cases and provider settings
2. **Processes Images**: Converts images to base64 for API calls
3. **Calls Providers**: Makes structured requests to each configured provider
4. **Captures Raw Responses**: Records authentic output from each API
5. **Measures Performance**: Tracks latency, tokens, and errors
6. **Saves Results**: Outputs detailed JSON results for analysis
7. **Compares Providers**: Shows summary of speed, cost, and success rates

## 🛠️ Requirements

- Python 3.8+
- API keys for desired providers
- Images in supported formats (JPG, PNG, GIF, WebP)

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

- 🐛 [Report Issues](https://github.com/realadeel/llm-test-bench/issues)
- 💡 [Request Features](https://github.com/realadeel/llm-test-bench/issues)
- 📖 [Documentation](https://realadeel.github.io/llm-test-bench/)

---

**Ready to benchmark your vision AI?** Start with the [Quick Start](#-quick-start) guide above! 🚀
