#!/usr/bin/env python3
"""
CLI tool for image analysis.

Usage:
    python scripts/analyze_image.py image.png
    python scripts/analyze_image.py document.jpg --prompt "Extract all text"
"""

import sys
import argparse
import logging
from pathlib import Path


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Analyze images and extract text using Claude Vision"
    )
    
    parser.add_argument(
        "image_file",
        help="Path to image file (PNG, JPG, GIF, WEBP)"
    )
    
    parser.add_argument(
        "--prompt",
        "-p",
        help="Custom analysis prompt (optional)"
    )
    
    parser.add_argument(
        "--extract-text",
        action="store_true",
        help="Focus on extracting text (OCR mode)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (optional, will save analysis)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Validate file
    image_path = Path(args.image_file)
    if not image_path.exists():
        print(f"❌ Error: File not found: {image_path}")
        sys.exit(1)
    
    # Determine prompt
    if args.extract_text:
        prompt = "Extract all text from this image. Preserve formatting."
    else:
        prompt = args.prompt
    
    print(f"\n{'='*60}")
    print(f"📸 Image Analysis")
    print(f"{'='*60}")
    print(f"File: {image_path.name}")
    if prompt:
        print(f"Prompt: {prompt}")
    print(f"{'='*60}\n")
    
    try:
        # Import and analyze
        from services import ImageService
        
        service = ImageService()
        
        if args.extract_text and not prompt:
            result = service.extract_text(image_path)
        else:
            result = service.analyze(image_path, prompt=prompt)
        
        # Print result
        print(f"\n{'='*60}")
        print("Analysis Result:")
        print(f"{'='*60}")
        print(result)
        print(f"{'='*60}\n")
        
        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result)
            print(f"💾 Saved to: {output_path}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
