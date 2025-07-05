# 📊 LLM Test Bench Documentation

Welcome to the comprehensive documentation for LLM Test Bench!

## 🚀 Quick Navigation

- **[Getting Started](getting-started.md)** - Installation and basic setup
- **[Configuration Guide](configuration.md)** - Advanced configuration options
- **[API Reference](api-reference.md)** - Detailed API documentation
- **[Examples](examples.md)** - Real-world usage examples
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

## 🌟 What is LLM Test Bench?

LLM Test Bench is a production-ready tool for comparing Large Language Model providers on vision tasks. It helps you:

- **Compare providers**: OpenAI, AWS Bedrock/Claude, Google Gemini
- **Optimize costs**: Track token usage and API costs
- **Measure performance**: Latency, accuracy, and reliability metrics
- **Deploy confidently**: Production-ready for Lambda and serverless

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

3. **Add test images to `test_images/`**

4. **Run the benchmark:**
```bash
python llm_test_bench.py
```

## 📈 Example Results

```
🎉 Test complete!
✅ Successful: 3
❌ Failed: 0
✅ openai: 1,250ms (1,240 tokens, $0.048)
✅ bedrock_claude: 890ms (980 tokens, $0.012)
✅ gemini: 1,100ms (1,150 tokens, $0.008)
```

## 🔗 Useful Links

- **[GitHub Repository](https://github.com/realadeel/llm-test-bench)**
- **[Issues & Bug Reports](https://github.com/realadeel/llm-test-bench/issues)**
- **[Contributing Guidelines](https://github.com/realadeel/llm-test-bench/blob/main/CONTRIBUTING.md)**
- **[License](https://github.com/realadeel/llm-test-bench/blob/main/LICENSE)**

## 💬 Community

- **GitHub Discussions**: Ask questions and share use cases
- **Issues**: Report bugs and request features
- **Pull Requests**: Contribute improvements

---

**Ready to start benchmarking?** Check out our [Getting Started Guide](getting-started.md)!
