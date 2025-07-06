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
        """Call Bedrock Claude API with tools for structured output"""
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
            
            # Handle multiple tools (let AI choose)
            if 'tools' in test_case:
                # Convert config tools to Bedrock format
                bedrock_tools = []
                for tool in test_case['tools']:
                    bedrock_tools.append({
                        "name": tool['name'],
                        "description": tool['description'],
                        "input_schema": tool['schema']
                    })
                
                body["tools"] = bedrock_tools
                body["tool_choice"] = {"type": "auto"}  # Let Claude choose the best tool
            
            # Handle single schema (legacy support)
            elif 'schema' in test_case:
                tool_name = test_case.get('name', 'structured_response').lower().replace(' ', '_')
                body["tools"] = [{
                    "name": tool_name,
                    "description": f"Analyze and respond with structured data according to the schema for: {test_case.get('name', 'this request')}",
                    "input_schema": test_case['schema']
                }]
                body["tool_choice"] = {
                    "type": "tool",
                    "name": tool_name
                }
            
            response = self.bedrock_client.invoke_model(
                modelId=test_case['model'],
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract response text based on response type
            if ('schema' in test_case or 'tools' in test_case) and 'content' in response_body:
                # Tool use response
                for content in response_body['content']:
                    if content['type'] == 'tool_use':
                        response_text = json.dumps(content['input'], indent=2)
                        break
                else:
                    response_text = response_body['content'][0]['text']
            else:
                # Regular text response
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
        """Call OpenAI API with tools/json_schema structured output"""
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
            
            # Handle multiple tools (let AI choose)
            if 'tools' in test_case:
                # Convert config tools to OpenAI function format
                openai_tools = []
                for tool in test_case['tools']:
                    openai_tools.append({
                        "type": "function",
                        "function": {
                            "name": tool['name'],
                            "description": tool['description'],
                            "parameters": tool['schema']
                        }
                    })
                
                body["tools"] = openai_tools
                body["tool_choice"] = "auto"  # Let OpenAI choose the best tool
            
            # Handle single schema (legacy support)
            elif 'schema' in test_case:
                # Use OpenAI's json_schema for structured output
                openai_schema = test_case['schema'].copy()
                
                # OpenAI strict mode requires ALL properties to be in required array
                if 'properties' in openai_schema:
                    openai_schema['required'] = list(openai_schema['properties'].keys())
                
                body["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": test_case.get('name', 'response').lower().replace(' ', '_'),
                        "strict": True,
                        "schema": openai_schema
                    }
                }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=self.openai_headers,
                    json=body
                ) as response:
                    response_data = await response.json()
                    
                    if response.status != 200:
                        raise Exception(f"OpenAI API error: {response_data}")
                    
                    # Extract response based on type
                    message = response_data['choices'][0]['message']
                    
                    if 'tools' in test_case and 'tool_calls' in message:
                        # Tool call response
                        tool_call = message['tool_calls'][0]
                        response_text = tool_call['function']['arguments']
                    elif 'schema' in test_case:
                        # JSON schema response
                        response_text = message['content']
                    else:
                        # Regular text response
                        response_text = message['content']
                    
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

    def _clean_schema_for_gemini(self, schema: Dict) -> Dict:
        """Remove fields that Gemini doesn't support from schema"""
        cleaned = schema.copy()
        
        # Remove additionalProperties - Gemini doesn't support it
        if 'additionalProperties' in cleaned:
            del cleaned['additionalProperties']
        
        # Recursively clean nested objects
        if 'properties' in cleaned:
            for prop_key, prop_value in cleaned['properties'].items():
                if isinstance(prop_value, dict):
                    cleaned['properties'][prop_key] = self._clean_schema_for_gemini(prop_value)
        
        if 'items' in cleaned and isinstance(cleaned['items'], dict):
            cleaned['items'] = self._clean_schema_for_gemini(cleaned['items'])
        
        return cleaned

    def _create_union_schema_for_gemini(self, tools: List[Dict]) -> Dict:
        """
        Create a union schema for Gemini that includes all possible fields from all tools.
        This allows the AI to output any combination of fields based on what it detects.
        """
        union_properties = {
            "item_type": {
                "type": "string",
                "enum": [tool["name"] for tool in tools],
                "description": "The type of analysis performed - which tool was conceptually used"
            }
        }
        
        all_required = ["item_type"]
        
        # Merge all properties from all tool schemas
        for tool in tools:
            schema = tool["schema"]
            if "properties" in schema:
                for prop_name, prop_def in schema["properties"].items():
                    if prop_name not in union_properties:
                        # Make all fields optional in the union except core ones
                        union_properties[prop_name] = prop_def.copy()
                
                # Add required fields from this tool to the union
                if "required" in schema:
                    for req_field in schema["required"]:
                        if req_field not in all_required:
                            all_required.append(req_field)
        
        return {
            "type": "object",
            "properties": union_properties,
            "required": all_required
        }

    async def _call_gemini(self, test_case: Dict) -> TestResult:
        """Call Gemini API with responseSchema for structured output"""
        start_time = time.time()
        
        try:
            image_b64 = self._load_image_as_base64(test_case['image_path'])
            mime_type = self._get_image_mime_type(test_case['image_path'])
            
            # Gemini request format
            body = {
                "contents": [
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
                ],
                "generationConfig": {
                    "maxOutputTokens": test_case.get('max_tokens', 2000),
                    "temperature": test_case.get('temperature', 0.7)
                }
            }
            
            # Handle multiple tools (use responseSchema instead of function calling)
            if 'tools' in test_case:
                # Create a union schema that includes all possible fields
                union_schema = self._create_union_schema_for_gemini(test_case['tools'])
                cleaned_schema = self._clean_schema_for_gemini(union_schema)
                # CRITICAL: Must set responseMimeType to application/json for schema to work
                body["generationConfig"]["responseMimeType"] = "application/json"
                body["generationConfig"]["responseSchema"] = cleaned_schema
            
            # Handle single schema (legacy support)
            elif 'schema' in test_case:
                # CRITICAL: Must set responseMimeType to application/json for schema to work
                body["generationConfig"]["responseMimeType"] = "application/json"
                body["generationConfig"]["responseSchema"] = self._clean_schema_for_gemini(test_case['schema'])
            
            api_key = os.getenv('GEMINI_API_KEY')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{test_case['model']}:generateContent?key={api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=self.gemini_headers,
                    json=body
                ) as response:
                    response_data = await response.json()
                    
                    if response.status != 200:
                        raise Exception(f"Gemini API error: {response_data}")
                    
                    # Extract response - should be direct JSON now
                    candidate = response_data['candidates'][0]
                    response_text = candidate['content']['parts'][0]['text']
                    
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
