# 🚀 LLM Test Bench

A production-ready benchmarking tool for comparing Large Language Model providers on vision tasks with structured output. Test OpenAI, AWS Bedrock Claude, and Google Gemini side-by-side to optimize performance, cost, and accuracy.

## ✨ Features

- **Multi-Provider Support**: Compare OpenAI GPT-4, AWS Bedrock Claude, and Google Gemini
- **Vision + Structured Output**: Test image analysis with deterministic JSON responses
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

- **Content Analysis**: Test how well each provider analyzes images, documents, or media
- **Structured Data Extraction**: Compare accuracy of extracting specific fields from images
- **Tool Selection**: Benchmark AI's ability to choose appropriate analysis methods
- **Cost Optimization**: Find the most cost-effective provider for your use case
- **Performance Testing**: Measure latency and reliability across providers

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/realadeel/llm-test-bench.git
cd llm-test-bench
pip install -r requirements.txt
```

### 2. Set Up API Keys
Create a `.env` file:
```bash
# Required: At least one provider
OPENAI_API_KEY=your_openai_key_here
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Configure Your Test
Copy and customize the config:
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your test cases
```

### 4. Add Test Images
```bash
# Add your images to test_images/
cp your_image.jpg test_images/
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
