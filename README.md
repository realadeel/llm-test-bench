# 🚀 LLM Test Bench

An optimized benchmarking tool for comparing Large Language Model providers during prompt engineering. Test OpenAI, AWS Bedrock, and Google Gemini side-by-side to optimize performance and accuracy across any content type.

## ✨ Features

- **Multi-Provider Support**: Compare OpenAI, AWS Bedrock (multiple models), and Google Gemini
- **Multiple Models Per Provider**: Test different model variants (e.g., GPT-4 Nano vs Mini, Claude Haiku vs Sonnet)
- **Vision Model Support**: Full support for Llama 4, Claude, Pixtral, GPT-4V, and Gemini vision models
- **Multi-Image Processing**: Process ALL images in test_images/ directory when no specific image is set
- **Flexible Input**: Test with text prompts, images, documents, or any content type
- **Structured Output Testing**: Compare how well each provider follows your JSON schemas
- **Multi-Tool Testing**: Let AI choose the best analysis method from multiple options
- **Modern API Integration**: Uses each provider's optimal structured output methods:
  - OpenAI: `json_schema` and function calling
  - Claude: Tool use with structured schemas  
  - Llama 4: Converse API with tool support for vision
  - Pixtral: Function calling with image analysis
  - Gemini: `responseSchema` with union types
- **Raw Response Comparison**: See authentic output formatting from each provider
- **Production Ready**: Async operations, error handling, rate limiting
- **Performance Tracking**: Monitor token usage and latency across providers
- **Configurable**: YAML-based test configuration with environment variables

## 🎯 Use Cases

- **Prompt Engineering**: Compare how different providers handle your prompts
- **Schema Validation**: Test which provider best follows your structured output requirements
- **Multi-Tool Selection**: Benchmark AI's ability to choose appropriate analysis methods
- **Vision Analysis**: Compare accuracy of image understanding across models
- **Performance Testing**: Measure latency and reliability across providers
- **Household Item Cataloging**: Test how well different models identify various household items
- **Model Comparison**: Find optimal cost/performance balance across model variants

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
# Add your test images to test_images/
cp your_album_covers/*.jpg test_images/
cp your_books/*.png test_images/

# Or process ALL existing images by commenting out image_path in config.yaml
```

### 5. Run Benchmark
```bash
python llm_test_bench.py
```

## 📊 Example Output

```
🎉 Test complete!
📊 Test Cases: 1
🖼️ Images Processed: 3
✅ Successful Provider Calls: 9
❌ Failed Provider Calls: 0

📝 Production-Optimized Multi-Tool Analysis (3 images):
  📸 album1:
    ✅ openai_gpt4_nano: 1101ms
    ✅ gemini_flash_lite: 987ms
    ✅ bedrock_haiku_3: 1234ms
  📸 album2:
    ✅ openai_gpt4_nano: 987ms
    ✅ gemini_flash_lite: 876ms
    ✅ bedrock_haiku_3: 1098ms
  📸 book:
    ✅ openai_gpt4_nano: 1045ms
    ✅ gemini_flash_lite: 934ms
    ✅ bedrock_haiku_3: 1176ms

📊 Results saved to results/test_results_2025-07-07_01-54-05.json
```

### Optimized JSON Structure

**Efficient format with prompt and tools stored once per test case:**

```json
[
  {
    "name": "Production-Optimized Multi-Tool Analysis",
    "prompt": "You are a professional appraiser...",  // STORED ONCE
    "max_tokens": 2000,
    "temperature": 0.1,
    "tools": [...], // STORED ONCE
    "is_multi_image": true,
    "image_results": [
      {
        "image_path": "test_images/album1.jpg",
        "provider_results": [
          {
            "provider": "openai_gpt4_nano",
            "model": "gpt-4.1-nano-2025-04-14",
            "response": "{...}",
            "latency_ms": 1101.5,
            "timestamp": "2025-07-07T01:53:52.253486",
            "error": null,
            "tokens_used": 107
          }
          // ... other providers
        ]
      },
      {
        "image_path": "test_images/album2.jpg",
        "provider_results": [
          // ... provider results for album2
        ]
      }
      // ... other images
    ]
  }
]
```

**Benefits:**
- 💾 **Maximum efficiency** (prompt + tools stored once per test case)
- 📁 **Perfect organization** (results grouped by test case, then by image)
- 🔍 **Easy analysis** (compare providers across all images in one test case)
- ⚙️ **Full compatibility** (all original data preserved)

## 🔧 Configuration

### Multi-Image Processing
Process ALL images in your test directory:

```yaml
test_cases:
  - name: "Batch Analysis"
    prompt: "Analyze this household item..."
    # image_path: "specific.jpg"  # Comment out to process ALL images
    tools:
      # ... your tools
```

**Result**: Automatically processes every `.jpg`, `.png`, `.gif`, `.webp` file in `test_images/`

### Multiple Models Per Provider
Test different model variants from the same provider:

```yaml
providers:
  # Multiple OpenAI models
  - name: "openai_gpt4_nano"
    model: "gpt-4.1-nano-2025-04-14"
  - name: "openai_gpt4_mini"
    model: "gpt-4.1-mini-2025-04-14"
  
  # Multiple Gemini models
  - name: "gemini_flash_lite"
    model: "gemini-2.0-flash-lite"
  - name: "gemini_pro"
    model: "gemini-1.5-pro"
    
  # Multiple Bedrock models
  - name: "bedrock_haiku_3"
    model: "anthropic.claude-3-haiku-20240307-v1:0"
  - name: "bedrock_sonnet_4"
    model: "us.anthropic.claude-sonnet-4-20250514-v1:0"
```

**Naming Convention**: Use pattern `{provider}_{model_family}_{variant}` for clear identification in results.

### Multi-Tool Testing
Let the AI choose the best analysis method:

```yaml
test_cases:
  - name: "Smart Item Analysis"
    prompt: "Examine this image and choose the appropriate analysis tool."
    image_path: "test_images/mystery_item.jpg"
    tools:
      - name: "analyze_vinyl_record"
        description: "For vinyl records and LPs"
        schema:
          type: "object"
          properties:
            title: {type: "string"}
            artist: {type: "string"}
            genre: {type: "string"}
            year: {type: "string"}
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
    prompt: "List all objects in this image."
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
├── test_images/          # Your test images (auto-processed when image_path not set)
├── results/              # Benchmark results (optimized JSON format)
├── docs/                 # Documentation
│   └── README.md          # Comprehensive documentation
└── requirements.txt      # Dependencies
```

## 🎛️ Advanced Configuration

### Provider configurations
```yaml
providers:
  # Multiple OpenAI models
  - name: "openai_gpt4_nano"
    model: "gpt-4.1-nano-2025-04-14"
  - name: "openai_gpt4_mini"
    model: "gpt-4.1-mini-2025-04-14"
  
  # Multiple Gemini models
  - name: "gemini_flash_lite"
    model: "gemini-2.0-flash-lite"
  - name: "gemini_pro"
    model: "gemini-1.5-pro"
    
  # Multiple Bedrock models
  - name: "bedrock_haiku_3"
    model: "anthropic.claude-3-haiku-20240307-v1:0"
  - name: "bedrock_sonnet_4"
    model: "us.anthropic.claude-sonnet-4-20250514-v1:0"
  - name: "bedrock_llama_4_maverick"
    model: "us.meta.llama4-maverick-17b-instruct-v1:0"

# Rate limiting
delay_between_calls: 1      # seconds between API calls
delay_between_test_cases: 2 # seconds between test cases
```

### Test Parameters
```yaml
test_cases:
  - name: "Custom Test"
    prompt: "Your analysis prompt..."
    image_path: "test_images/image.jpg"  # Or comment out for multi-image
    max_tokens: 2000
    temperature: 0.7
    # ... schema or tools
```

## 🔍 How It Works

1. **Loads Configuration**: Reads your test cases and provider settings from YAML
2. **Processes Images**: Converts images to base64 for API calls  
3. **Smart API Selection**: Uses optimal API for each model (Converse for Llama 4 vision, InvokeModel for others)
4. **Structured Requests**: Converts your tool schemas to each provider's format
5. **Captures Raw Responses**: Records authentic JSON output from each API
6. **Measures Performance**: Tracks latency, tokens, and success rates
7. **Optimized Storage**: Groups results by test case for efficient analysis
8. **Saves Results**: Outputs organized JSON results for comparison

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
