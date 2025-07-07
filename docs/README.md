# 📊 LLM Test Bench Documentation

Welcome to the comprehensive documentation for LLM Test Bench!

## 🚀 Quick Navigation

- **[Quick Start](#-quick-start)** - Get running in 5 minutes
- **[Configuration Guide](#-configuration-guide)** - Set up your tests and providers
- **[Multi-Image Processing](#-multi-image-processing)** - Process entire image directories
- **[Multiple Models Per Provider](#-multiple-models-per-provider)** - Test model variants
- **[Multi-Tool Testing](#-multi-tool-testing)** - Let AI choose analysis methods
- **[Structured Output](#-structured-output)** - Traditional single-schema testing
- **[API Reference](#-api-reference)** - Detailed configuration options
- **[Troubleshooting](#-troubleshooting)** - Common issues and solutions

## 🌟 What is LLM Test Bench?

LLM Test Bench is a production-ready tool for comparing Large Language Model providers on vision tasks with structured output. It helps you:

- **Compare providers**: OpenAI, AWS Bedrock (multiple models), Google Gemini
- **Test model variants**: Compare different versions like GPT-4 Nano vs Mini, Claude Haiku vs Sonnet
- **Vision Model Support**: Test Llama 4, Claude, Pixtral, GPT-4V, and Gemini vision models
- **Process multiple images**: Batch process entire directories automatically
- **Test structured output**: JSON schemas, multi-tool selection, function calling
- **Measure performance**: Latency, accuracy, token usage
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
# Provider configurations - supports multiple vision models
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

## 🖼️ Multi-Image Processing

Process ALL images in the `test_images/` directory automatically when no specific image is configured.

### How It Works

**Single Image Mode:**
```yaml
test_cases:
  - name: "Specific Image Test"
    prompt: "Analyze this specific image..."
    image_path: "test_images/sample_image.jpg"  # Process only this image
```

**Multi-Image Mode:**
```yaml
test_cases:
  - name: "Batch Analysis"
    prompt: "Analyze this object..."
    # image_path: commented out or removed
```

**Result**: Automatically processes every `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` file in `test_images/`

### Benefits

- **Batch Processing**: Test prompts against multiple images at once
- **Comprehensive Testing**: See how well your tools work across different content types
- **Zero Configuration**: Just comment out `image_path` to enable
- **Flexible**: Mix single-image and multi-image test cases in the same config

### Output Structure

Results are organized by test case with all images grouped together:

```json
{
  "name": "Batch Analysis",
  "prompt": "Analyze this object...",  // STORED ONCE
  "tools": [...],                            // STORED ONCE
  "is_multi_image": true,
  "image_results": [
    {
      "image_path": "test_images/image1.jpg",
      "provider_results": [...]
    },
    {
      "image_path": "test_images/image2.jpg",
      "provider_results": [...]
    }
  ]
}
```

## 🔄 Multiple Models Per Provider

Test different model variants from the same provider to find the optimal cost/performance balance.

### Naming Convention

Use descriptive names following the pattern: `{provider}_{model_family}_{variant}`

```yaml
providers:
  # OpenAI variants
  - name: "openai_gpt4_nano"     # Fast, cheap
    model: "gpt-4.1-nano-2025-04-14"
  - name: "openai_gpt4_mini"     # Better quality
    model: "gpt-4.1-mini-2025-04-14"
  
  # Gemini variants
  - name: "gemini_flash_lite"    # Good balance
    model: "gemini-2.0-flash-lite"
  - name: "gemini_pro"           # Best quality
    model: "gemini-1.5-pro"
    
  # Bedrock variants
  - name: "bedrock_haiku_3"      # Fast Claude
    model: "anthropic.claude-3-haiku-20240307-v1:0"
  - name: "bedrock_sonnet_4"     # Best Claude
    model: "us.anthropic.claude-sonnet-4-20250514-v1:0"
```

### Benefits

- **Clear Identification**: Model variants clearly labeled in results
- **Easy Comparison**: Compare performance and cost across variants
- **Flexible Testing**: Enable/disable specific models easily
- **Cost Optimization**: Find the best price/performance ratio

### Example Output

```
📝 Object Analysis (3 images):
  📸 image1:
    ✅ openai_gpt4_nano: 1101ms     # Fast, cheap
    ✅ openai_gpt4_mini: 1307ms     # Better quality
    ✅ gemini_flash_lite: 987ms     # Good balance
    ✅ bedrock_haiku_3: 1234ms      # Fast Claude
    ✅ bedrock_sonnet_4: 2145ms     # Best Claude
```

## 🔧 Multi-Tool Testing

The most powerful feature - let the AI examine an image and choose the most appropriate analysis method from multiple options.

### How It Works

1. **You define multiple analysis tools** in your config
2. **AI examines the image** and determines what type of content it sees
3. **AI chooses the best tool** for analysis
4. **AI provides structured output** using the chosen tool's schema

### Example Configuration

```yaml
test_cases:
  - name: "Smart Object Analysis"
    prompt: "Examine this image carefully and choose the most appropriate analysis tool based on what you see."
    # image_path: commented out for multi-image processing
    tools:
      - name: "analyze_media_content"
        description: "For digital media files, images, and multimedia content"
        schema:
          type: "object"
          properties:
            title: {type: "string", description: "Content title or name"}
            creator: {type: "string", description: "Creator or author name"}
            category: {type: "string", description: "Content category"}
            year: {type: "string", description: "Creation or publication year"}
            source: {type: "string", description: "Source or publisher"}
          required: ["title", "creator"]
          
      - name: "analyze_publication"
        description: "For printed materials, documents, and publications"
        schema:
          type: "object"
          properties:
            title: {type: "string", description: "Publication title"}
            author: {type: "string", description: "Author or creator name"}
            publisher: {type: "string", description: "Publishing organization"}
            identifier: {type: "string", description: "ID number if visible"}
          required: ["title", "author"]
          
      - name: "analyze_product"
        description: "For consumer products, merchandise, and branded items"
        schema:
          type: "object"
          properties:
            name: {type: "string", description: "Product name or description"}
            brand: {type: "string", description: "Brand or manufacturer"}
            category: {type: "string", description: "Type of product"}
            estimated_value: {type: "string", description: "Estimated value range"}
          required: ["name", "brand"]
```

### Expected Output

```json
{
  "item_type": "analyze_media_content",
  "title": "Sample Content", 
  "creator": "Content Creator",
  "category": "Digital Media",
  "year": "2024",
  "source": "Digital Platform"
}
```

## 📋 Structured Output

For traditional single-schema testing, define a specific JSON schema:

```yaml
test_cases:
  - name: "Object Detection"
    prompt: "List all objects visible in this image with confidence scores."
    image_path: "test_images/scene.jpg"
    schema:
      type: "object"
      properties:
        objects:
          type: "array"
          items:
            properties:
              name: {type: "string"}
              confidence: {type: "number", minimum: 0, maximum: 1}
              location: {type: "string"}
        total_count: {type: "integer"}
        image_quality: {type: "string"}
      required: ["objects", "total_count"]
```

## 📊 Example Results

```
🎉 Test complete!
📊 Test Cases: 1
🖼️ Images Processed: 3
✅ Successful Provider Calls: 15  # 3 images × 5 models
❌ Failed Provider Calls: 0

📝 Smart Object Analysis (3 images):
  📸 image1:
    ✅ openai_gpt4_nano: 1101ms
    ✅ openai_gpt4_mini: 1307ms
    ✅ gemini_flash_lite: 987ms
    ✅ bedrock_haiku_3: 1234ms
    ✅ bedrock_sonnet_4: 2145ms
  📸 image2:
    ✅ openai_gpt4_nano: 923ms
    ✅ openai_gpt4_mini: 1156ms
    ✅ gemini_flash_lite: 876ms
    ✅ bedrock_haiku_3: 1098ms
    ✅ bedrock_sonnet_4: 1987ms
  📸 image3:
    ✅ openai_gpt4_nano: 1045ms
    ✅ openai_gpt4_mini: 1445ms
    ✅ gemini_flash_lite: 934ms
    ✅ bedrock_haiku_3: 1176ms
    ✅ bedrock_sonnet_4: 2234ms

📊 Results saved to results/test_results_2025-07-07_02-15-30.json
```

### Optimized JSON Structure

Results are organized by test case with maximum efficiency:

```json
[
  {
    "name": "Smart Object Analysis",
    "prompt": "Examine this image carefully...",  // STORED ONCE
    "max_tokens": 2000,
    "temperature": 0.1,
    "tools": [...],                              // STORED ONCE
    "is_multi_image": true,
    "image_results": [
      {
        "image_path": "test_images/image1.jpg",
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

## 🔗 API Reference

### Test Case Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Test case name for identification |
| `prompt` | string | Instructions for the AI |
| `image_path` | string | Path to test image (optional - comment out for multi-image) |
| `max_tokens` | integer | Maximum response tokens (default: 2000) |
| `temperature` | float | Response creativity (0.0-1.0, default: 0.7) |
| `tools` | array | Multiple analysis tools (multi-tool mode) |
| `schema` | object | Single JSON schema (traditional mode) |

### Provider Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Provider identifier - use descriptive names for multiple models |
| `model` | string | Specific model to use |

**Provider Name Patterns:**
- `openai_*` - Uses OpenAI API (e.g., `openai_gpt4_nano`, `openai_gpt4_mini`)
- `gemini_*` - Uses Google Gemini API (e.g., `gemini_flash_lite`, `gemini_pro`)
- `bedrock_*` - Uses AWS Bedrock (e.g., `bedrock_haiku_3`, `bedrock_sonnet_4`)
- Legacy names `openai` and `gemini` still supported

### Tool Schema

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Tool function name |
| `description` | string | When to use this tool (helps AI choose correctly) |
| `schema` | object | JSON schema for output structure |

## 🏗️ Advanced Features

### Multiple Bedrock Models

Test any Bedrock model by using provider names that start with `bedrock_`:

```yaml
providers:
  # Claude models
  - name: "bedrock_haiku_3"
    model: "anthropic.claude-3-haiku-20240307-v1:0"
  - name: "bedrock_sonnet_3_5"
    model: "anthropic.claude-3-5-sonnet-20241022-v2:0"
  - name: "bedrock_sonnet_4"
    model: "us.anthropic.claude-sonnet-4-20250514-v1:0"
  
  # Other Bedrock models
  - name: "bedrock_llama_4_maverick"
    model: "us.meta.llama4-maverick-17b-instruct-v1:0"
  - name: "bedrock_pixtral_large"
    model: "us.mistral.pixtral-large-2502-v1:0"
```

### Provider-Specific Features

- **OpenAI**: Uses `json_schema` with strict mode and function calling
- **Claude**: Uses tool schemas with auto selection
- **Llama 4**: Uses Converse API with tool support for vision tasks
- **Pixtral**: Uses function calling with image analysis
- **Gemini**: Uses `responseSchema` with union types for multi-tool

### Rate Limiting

Configure delays to respect API limits:

```yaml
delay_between_calls: 1      # Wait between provider calls
delay_between_test_cases: 2 # Wait between different tests
```

## 🛠️ Troubleshooting

### Common Issues

**API Key Errors**: 
- Ensure your `.env` file has the correct keys and is in the project root
- Check for specific error messages:
  - `"OPENAI_API_KEY not configured"` - Add OpenAI key to `.env`
  - `"GEMINI_API_KEY not configured"` - Add Gemini key to `.env`
  - `"AWS credentials not configured"` - Add AWS keys to `.env`

**Image Format**: 
- Supported formats are JPG, PNG, GIF, WebP
- Ensure images are in `test_images/` directory
- Check file permissions

**Schema Errors**: 
- Validate your JSON schemas using online tools
- Remember Gemini doesn't support `additionalProperties`
- Use simple, clear property names

**Provider Skipping**:
- Use descriptive provider names like `openai_gpt4_nano` instead of `openai`
- Check that provider name starts with correct prefix (`openai_`, `gemini_`, `bedrock_`)

**Bedrock Errors**:
- Check AWS region is correct (default: us-east-1)
- Ensure model IDs are exact and current
- Verify Bedrock access permissions in AWS console

**Response Formatting**: 
- Each provider formats JSON differently - this is expected behavior
- OpenAI tends toward compact JSON, while Gemini may include newlines for readability

**Rate Limiting**: 
- Increase delay values if you hit rate limits
- Consider using fewer models or images for initial testing

### Getting Help

- 🐛 [Report Issues](https://github.com/realadeel/llm-test-bench/issues)
- 💡 [Request Features](https://github.com/realadeel/llm-test-bench/issues)
- 📖 [View Source](https://github.com/realadeel/llm-test-bench)

---

**Ready to start benchmarking?** Check out the example configuration in `config.yaml.example`! 🚀
