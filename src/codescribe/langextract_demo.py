"""
LangExtract Demo Script for CodeScribe

This script demonstrates how to use the LangExtract library for structured data extraction
from unstructured text using Google's Gemini models.
"""

import os
import textwrap
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    import langextract as lx
except ImportError:
    print("LangExtract library not found. Install it with: uv add langextract")
    exit(1)

from src.codescribe.config import config


def setup_api_key() -> None:
    """Set up API key for LangExtract with AI Studio."""
    if not config.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    os.environ["LANGEXTRACT_API_KEY"] = config.GOOGLE_API_KEY
    
    # Ensure we're using AI Studio (not Vertex AI)
    if "GOOGLE_GENAI_USE_VERTEXAI" in os.environ:
        del os.environ["GOOGLE_GENAI_USE_VERTEXAI"]
    
    print("✅ Configured for AI Studio with API key")
    print("✅ Using Generative Language API endpoint")


def setup_oauth_credentials() -> None:
    """Set up OAuth credentials for LangExtract with Vertex AI using .env configuration."""
    # Load ADC parameters from .env file
    use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    genai_project_id = os.getenv("GOOGLE_GENAI_PROJECT_ID")
    
    if not all([project_id, location, credentials_path]):
        raise ValueError("Missing required ADC configuration in .env file")
    
    # CRITICAL: Remove GOOGLE_API_KEY that interferes with OAuth, but keep LANGEXTRACT_API_KEY
    conflicting_vars = ["GOOGLE_API_KEY", "GOOGLE_GENAI_API_KEY"]
    for var in conflicting_vars:
        if var in os.environ:
            del os.environ[var]
            print(f"🗑️  Removed conflicting {var} environment variable")
    
    # Ensure LANGEXTRACT_API_KEY is set from .env (LangExtract requires this even for OAuth)
    langextract_key = os.getenv("LANGEXTRACT_API_KEY")
    if langextract_key:
        os.environ["LANGEXTRACT_API_KEY"] = langextract_key
        print("✅ Set LANGEXTRACT_API_KEY for LangExtract (required even with OAuth)")
    
    # Set environment variables for LangExtract OAuth
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(use_vertexai)
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = location
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    
    if genai_project_id:
        os.environ["GOOGLE_GENAI_PROJECT_ID"] = genai_project_id
    
    print("✅ Configured for Vertex AI with OAuth credentials from .env")
    print(f"✅ Project: {project_id}")
    print(f"✅ Location: {location}")
    print(f"✅ Credentials: {credentials_path}")
    print("✅ Using OAuth - no API keys required")


def create_extraction_prompt() -> str:
    """Create a detailed prompt for entity extraction."""
    return textwrap.dedent("""\
        Extract people's names, AI models, products, and company names in order of appearance.
        Use exact text for extractions. Do not paraphrase or overlap entities.
        Provide meaningful related entities for each entity to add context.""")


def create_few_shot_examples() -> List[lx.data.ExampleData]:
    """Create few-shot examples to guide the model."""
    return [
        lx.data.ExampleData(
            text=(
                "David Ha from Sakana AI labs has trained many models"
                " including the early 'WM1' and his company makes a product called 'AI Scientist'."
            ),
            extractions=[
                lx.data.Extraction(
                    extraction_class="person_name",
                    extraction_text="David Ha",
                    attributes={"company": "Sakana AI"},
                ),
                lx.data.Extraction(
                    extraction_class="company_name",
                    extraction_text="Sakana AI",
                    attributes={"employee": "David Ha"},
                ),
                lx.data.Extraction(
                    extraction_class="ai_model",
                    extraction_text="WM1",
                    attributes={"company": "Sakana AI"},
                ),
                lx.data.Extraction(
                    extraction_class="product",
                    extraction_text="'AI Scientist'",
                    attributes={"company": "Sakana AI"},
                ),
            ]
        )
    ]


def get_sample_text() -> str:
    """Return sample text for extraction."""
    return textwrap.dedent("""\
        Shortly after Hunter Lightman joined OpenAI as a researcher in 2022, he watched his 
        colleagues launch ChatGPT, one of the fastest-growing products ever. The breakthrough 
        came from the GPT-4 model that Sam Altman's team had been developing. Meanwhile, 
        Demis Hassabis at DeepMind was working on Gemini, Google's answer to ChatGPT. 
        Elon Musk, who had previously co-founded OpenAI, launched his own AI company called xAI 
        with their Grok model. Meta's Mark Zuckerberg recruited five of the o1 researchers 
        to work on Meta's new superintelligence-focused unit developing the Llama models.
        """)


def run_extraction(text: str, prompt: str, examples: List[lx.data.ExampleData], 
                  model_id: str = "gemini-2.5-flash") -> Any:
    """Run the LangExtract extraction process."""
    print(f"🔍 Running extraction with model: {model_id}")
    print(f"📝 Text length: {len(text)} characters")
    print("-" * 50)
    
    try:
        # LangExtract will automatically use LANGEXTRACT_API_KEY environment variable
        result = lx.extract(
            text_or_documents=text,
            prompt_description=prompt,
            examples=examples,
            model_id=model_id
        )
        return result
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return None


def display_results(result: Any) -> None:
    """Display extraction results in a structured format."""
    if not result or not hasattr(result, 'extractions'):
        print("❌ No results to display")
        return
    
    # Group extractions by class
    grouped_results: Dict[str, List[Any]] = {}
    for extraction in result.extractions:
        class_name = extraction.extraction_class
        if class_name not in grouped_results:
            grouped_results[class_name] = []
        grouped_results[class_name].append(extraction)
    
    # Display results by category
    for class_name, extractions in grouped_results.items():
        print(f"\n📊 {class_name.replace('_', ' ').title()}s Found: {len(extractions)}")
        print("=" * 40)
        
        for i, extraction in enumerate(extractions, 1):
            print(f"{i}. {extraction.extraction_text}")
            if hasattr(extraction, 'attributes') and extraction.attributes:
                print(f"   Attributes: {extraction.attributes}")
            if hasattr(extraction, 'char_interval'):
                print(f"   Position: {extraction.char_interval}")
            print("-" * 20)


def main() -> None:
    """Main function to run the LangExtract demo."""
    print("🚀 CodeScribe LangExtract Demo")
    print("=" * 50)
    
    try:
        # Check if we should use Vertex AI (OAuth) or AI Studio (API key)
        use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False").lower() == "true"
        
        if use_vertexai:
            # Setup OAuth credentials for Vertex AI from .env
            setup_oauth_credentials()
        else:
            # Setup API key for AI Studio
            setup_api_key()
        
        # Create prompt and examples
        prompt = create_extraction_prompt()
        examples = create_few_shot_examples()
        print("✅ Prompt and examples created")
        
        # Get sample text
        sample_text = get_sample_text()
        print("✅ Sample text loaded")
        
        # Run extraction
        result = run_extraction(sample_text, prompt, examples)
        
        if result:
            print("✅ Extraction completed successfully!")
            display_results(result)
        else:
            print("❌ Extraction failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set your GOOGLE_API_KEY in the .env file")
        print("2. Installed langextract: uv add langextract")


if __name__ == "__main__":
    main()
