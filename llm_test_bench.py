import json
import asyncio
import aiohttp
import boto3
import base64
import time
import logging
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import yaml
from dataclasses import dataclass, asdict

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    provider: str
    model: str
    prompt: str
    response: str
    latency_ms: float
    timestamp: str
    error: Optional[str] = None
    tokens_used: Optional[int] = None

class LLMTestBench:
    def __init__(self, config_path: str = 'config.yaml'):
        if not Path(config_path).exists():
            if Path('config.yaml.example').exists():
                print("❌ config.yaml not found!")
                print("📋 Please copy config.yaml.example to config.yaml:")
                print("   cp config.yaml.example config.yaml")
                print("   # Then edit config.yaml with your test cases")
                exit(1)
            else:
                print("❌ No configuration file found!")
                print("📋 Please create config.yaml with your test configuration.")
                exit(1)
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize clients
        self.bedrock_client = None
        self.openai_headers = None
        self.gemini_headers = None
        
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize API clients - secrets from .env"""
        
        # Bedrock setup
        if os.getenv('AWS_ACCESS_KEY_ID'):
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_REGION', 'us-east-1'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
        
        # OpenAI setup
        if os.getenv('OPENAI_API_KEY'):
            self.openai_headers = {
                'Authorization': f"Bearer {os.getenv('OPENAI_API_KEY')}",
                'Content-Type': 'application/json'
            }
        
        # Gemini setup
        if os.getenv('GEMINI_API_KEY'):
            self.gemini_headers = {
                'Content-Type': 'application/json'
            }
    
    def _load_image_as_base64(self, image_path: str) -> str:
        """Load image file and convert to base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _get_image_mime_type(self, image_path: str) -> str:
        """Determine MIME type from file extension"""
        ext = Path(image_path).suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'image/jpeg')
    
    async def _call_bedrock_claude(self, test_case: Dict) -> TestResult:
        """Call Bedrock Claude API"""
        start_time = time.time()
        
        try:
            image_b64 = self._load_image_as_base64(test_case['image_path'])
            mime_type = self._get_image_mime_type(test_case['image_path'])
            
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": test_case['prompt']
                    }
                ]
            }
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": test_case.get('max_tokens', 2000),
                "temperature": test_case.get('temperature', 0.7),
                "messages": [message]
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=test_case['model'],
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']
            latency = (time.time() - start_time) * 1000
            
            return TestResult(
                provider="bedrock_claude",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response=response_text,
                latency_ms=latency,
                timestamp=datetime.now().isoformat(),
                tokens_used=response_body.get('usage', {}).get('output_tokens', 0)
            )
            
        except Exception as e:
            logger.error(f"Bedrock Claude error: {str(e)}")
            return TestResult(
                provider="bedrock_claude",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response="",
                latency_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )
    
    async def _call_openai(self, test_case: Dict) -> TestResult:
        """Call OpenAI API"""
        start_time = time.time()
        
        try:
            image_b64 = self._load_image_as_base64(test_case['image_path'])
            mime_type = self._get_image_mime_type(test_case['image_path'])
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": test_case['prompt']
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_b64}"
                            }
                        }
                    ]
                }
            ]
            
            body = {
                "model": test_case['model'],
                "messages": messages,
                "max_tokens": test_case.get('max_tokens', 2000),
                "temperature": test_case.get('temperature', 0.7)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=self.openai_headers,
                    json=body
                ) as response:
                    response_data = await response.json()
            
            if 'error' in response_data:
                raise Exception(f"OpenAI API error: {response_data['error']['message']}")
            
            response_text = response_data['choices'][0]['message']['content']
            latency = (time.time() - start_time) * 1000
            
            return TestResult(
                provider="openai",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response=response_text,
                latency_ms=latency,
                timestamp=datetime.now().isoformat(),
                tokens_used=response_data.get('usage', {}).get('total_tokens', 0)
            )
            
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            return TestResult(
                provider="openai",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response="",
                latency_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )
    
    async def _call_gemini(self, test_case: Dict) -> TestResult:
        """Call Gemini API"""
        start_time = time.time()
        
        try:
            image_b64 = self._load_image_as_base64(test_case['image_path'])
            mime_type = self._get_image_mime_type(test_case['image_path'])
            
            contents = [
                {
                    "parts": [
                        {
                            "text": test_case['prompt']
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_b64
                            }
                        }
                    ]
                }
            ]
            
            body = {
                "contents": contents,
                "generationConfig": {
                    "maxOutputTokens": test_case.get('max_tokens', 2000),
                    "temperature": test_case.get('temperature', 0.7)
                }
            }
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_case['model']}:generateContent"
            params = {"key": os.getenv('GEMINI_API_KEY')}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    params=params,
                    headers=self.gemini_headers,
                    json=body
                ) as response:
                    response_data = await response.json()
            
            if 'error' in response_data:
                raise Exception(f"Gemini API error: {response_data['error']['message']}")
            
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            latency = (time.time() - start_time) * 1000
            
            return TestResult(
                provider="gemini",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response=response_text,
                latency_ms=latency,
                timestamp=datetime.now().isoformat(),
                tokens_used=response_data.get('usageMetadata', {}).get('totalTokenCount', 0)
            )
            
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return TestResult(
                provider="gemini",
                model=test_case['model'],
                prompt=test_case['prompt'],
                response="",
                latency_ms=(time.time() - start_time) * 1000,
                timestamp=datetime.now().isoformat(),
                error=str(e)
            )
    
    async def run_test_case(self, test_case: Dict) -> List[TestResult]:
        """Run a single test case across all configured providers"""
        results = []
        
        for provider_config in self.config['providers']:
            provider_name = provider_config['name']
            model = provider_config['model']
            
            # Create test case with provider-specific model
            test_case_copy = test_case.copy()
            test_case_copy['model'] = model
            
            if provider_name == 'bedrock_claude' and self.bedrock_client:
                result = await self._call_bedrock_claude(test_case_copy)
            elif provider_name == 'openai' and self.openai_headers:
                result = await self._call_openai(test_case_copy)
            elif provider_name == 'gemini' and self.gemini_headers:
                result = await self._call_gemini(test_case_copy)
            else:
                continue  # Skip if no API key
            
            results.append(result)
            
            # Add delay between API calls
            await asyncio.sleep(self.config.get('delay_between_calls', 1))
        
        return results
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all test cases"""
        all_results = []
        
        for i, test_case in enumerate(self.config['test_cases']):
            logger.info(f"Running test case {i+1}/{len(self.config['test_cases'])}: {test_case.get('name', 'Unnamed')}")
            
            results = await self.run_test_case(test_case)
            all_results.extend(results)
            
            # Add delay between test cases
            if i < len(self.config['test_cases']) - 1:
                await asyncio.sleep(self.config.get('delay_between_test_cases', 2))
        
        return all_results
    
    def save_results(self, results: List[TestResult], output_file: str):
        """Save test results to JSON file"""
        results_dict = [asdict(result) for result in results]
        
        with open(output_file, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")

# Simple runner
async def main():
    test_bench = LLMTestBench()
    results = await test_bench.run_all_tests()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'results/test_results_{timestamp}.json'
    test_bench.save_results(results, output_file)
    
    # Print summary
    successful = [r for r in results if r.error is None]
    failed = [r for r in results if r.error is not None]
    
    print(f"\n🎉 Test complete!")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    for result in results:
        status = "✅" if result.error is None else "❌"
        print(f"{status} {result.provider}: {result.latency_ms:.0f}ms")

if __name__ == "__main__":
    asyncio.run(main())
