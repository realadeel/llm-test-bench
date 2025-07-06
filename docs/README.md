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

- **Compare providers**: OpenAI, AWS Bedrock/Claude, Google Gemini
- **Test structured output**: JSON schemas, multi-tool selection, function calling
- **Measure performance**: Latency, accuracy, token usage, and cost
- **Deploy confidently**: Production-ready for Lambda and serverless environments

## 🏃‍♂️ Quick Start

1. **Clone and install:**
```bash
git clone https://github.com/realadeel/llm-test-bench.git
cd llm-test-bench
pip install -r requirements.txt
```

2. **Set up API keys in `.env`:**
```bash
OPENAI_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
GEMINI_API_KEY=your_gemini_key
```

3. **Configure your tests:**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your test cases
```

4. **Add test images to `test_images/`**

5. **Run the benchmark:**
```bash
python llm_test_bench.py
```

## ⚙️ Configuration Guide

### Basic Setup

Your `config.yaml` file controls which providers to test and what tests to run:

```yaml
# Provider configurations
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

### Environment Variables

Create a `.env` file with your API credentials:

```bash
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# AWS Bedrock
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1

# Google Gemini
GEMINI_API_KEY=your-gemini-key
```

## 🔧 Multi-Tool Testing

The most powerful feature of LLM Test Bench is multi-tool testing, where the AI examines an image and chooses the most appropriate analysis method from multiple options.

### How It Works

1. **You define multiple analysis tools** in your config
2. **AI examines the image** and determines what type of content it sees
3. **AI chooses the best tool** for analysis
4. **AI provides structured output** using the chosen tool's schema

### Example Configuration

```yaml
test_cases:
  - name: "Multi-Tool Analysis"
    prompt: "Examine this image and choose the appropriate analysis tool."
    image_path: "test_images/album_cover.jpg"
    tools:
      - name: "analyze_music_album"
        description: "For vinyl records, CDs, and music items"
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

### Expected Output

```json
{
  "item_type": "analyze_music_album",
  "title": "OK Computer", 
  "artist": "Radiohead",
  "genre": "Alternative Rock",
  "year": "1997"
}
```

## 📋 Structured Output

For traditional single-schema testing, you can define a specific JSON schema:

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

## 📈 Example Results

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

## 🔗 API Reference

### Test Case Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Test case name for identification |
| `prompt` | string | Instructions for the AI |
| `image_path` | string | Path to test image |
| `max_tokens` | integer | Maximum response tokens (default: 2000) |
| `temperature` | float | Response creativity (0.0-1.0, default: 0.7) |
| `tools` | array | Multiple analysis tools (multi-tool mode) |
| `schema` | object | Single JSON schema (traditional mode) |

### Provider Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Provider identifier (`openai`, `bedrock_claude`, `gemini`) |
| `model` | string | Specific model to use |

### Tool Schema

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Tool function name |
| `description` | string | When to use this tool |
| `schema` | object | JSON schema for output structure |

## 🚀 Advanced Features

### Provider-Specific Features

- **OpenAI**: Uses `json_schema` with strict mode and function calling
- **Bedrock Claude**: Uses tool schemas with auto selection
- **Gemini**: Uses `responseSchema` with union types for multi-tool

### Rate Limiting

Configure delays to respect API limits:

```yaml
delay_between_calls: 1      # Wait between provider calls
delay_between_test_cases: 2 # Wait between different tests
```

### Results Format

Results are saved as JSON with detailed metrics:

```json
{
  "provider": "openai",
  "model": "gpt-4o-mini", 
  "prompt": "...",
  "response": "{...}",
  "latency_ms": 1417.08,
  "timestamp": "2025-07-05T20:07:05.146788",
  "tokens_used": 539,
  "error": null
}
```

## 🛠️ Troubleshooting

### Common Issues

**API Key Errors**: Ensure your `.env` file has the correct keys and is in the project root.

**Image Format**: Supported formats are JPG, PNG, GIF, WebP. Ensure images are in `test_images/` directory.

**Schema Errors**: Validate your JSON schemas using online tools. Remember Gemini doesn't support `additionalProperties`.

**Rate Limiting**: Increase delay values if you hit rate limits.

### Getting Help

- 🐛 [Report Issues](https://github.com/realadeel/llm-test-bench/issues)
- 💡 [Request Features](https://github.com/realadeel/llm-test-bench/issues)
- 📖 [View Source](https://github.com/realadeel/llm-test-bench)

---

**Ready to start benchmarking?** Check out the example configuration in `config.yaml.example`! 🚀
