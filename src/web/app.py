"""
AI Content Processor Web Application.

Provides a user-friendly web interface for:
1. Audio transcription
2. Image analysis
3. Document processing
"""

import os
import sys
import logging

# Fix OpenMP conflict before any other imports
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import gradio as gr
from config import settings

logger = logging.getLogger(__name__)


def transcribe_audio(audio_file_path):
    """
    Transcribe audio file to text.
    
    Args:
        audio_file_path: Path to uploaded audio file
        
    Returns:
        Transcription result or error message
    """
    if audio_file_path is None:
        return "⚠️ Please upload an audio file."
    
    try:
        # Lazy import to avoid initialization issues
        from services import AudioService
        
        logger.info(f"🎤 Processing audio: {audio_file_path}")
        
        service = AudioService()
        result = service.transcribe(audio_file_path)
        
        return result.text
        
    except Exception as e:
        error_msg = f"❌ Error during transcription: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def analyze_image(image_file, prompt):
    """
    Analyze image and extract information.
    
    Args:
        image_file: Path to uploaded image file
        prompt: Optional analysis prompt
        
    Returns:
        Analysis result or error message
    """
    if image_file is None:
        return "⚠️ Please upload an image file."
    
    try:
        # Lazy import
        from services import ImageService
        
        logger.info(f"📸 Processing image: {image_file}")
        
        service = ImageService()
        result = service.analyze(image_file, prompt=prompt if prompt else None)
        
        return result
        
    except Exception as e:
        error_msg = f"❌ Error during image analysis: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def generate_meeting_minutes(transcript):
    """
    Generate meeting minutes from transcript.
    
    Args:
        transcript: Meeting transcript text
        
    Returns:
        Meeting minutes or error message
    """
    if not transcript or not transcript.strip():
        return "⚠️ Please enter a transcript."
    
    try:
        from services import DocumentService
        
        logger.info("📝 Generating meeting minutes...")
        
        service = DocumentService()
        result = service.generate_meeting_minutes(transcript)
        
        return result
        
    except Exception as e:
        error_msg = f"❌ Error generating minutes: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


def create_interface():
    """
    Create the Gradio interface.
    
    Returns:
        Gradio Blocks interface
    """
    with gr.Blocks(
        title="AI Content Processor"
    ) as demo:
        
        gr.Markdown(
            """
            # 🎙️📸📝 AI Content Processor
            ### Process audio, images, and text with AI
            """
        )
        
        with gr.Tabs():
            # Tab 1: Audio Transcription
            with gr.Tab("🎙️ Audio Transcription"):
                gr.Markdown(
                    """
                    ### Transcribe audio files using Whisper AI
                    Supports: WAV, MP3, M4A, FLAC, OGG, and more
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        audio_input = gr.Audio(
                            type="filepath",
                            label="Upload Audio File"
                        )
                        audio_button = gr.Button(
                            "🎤 Transcribe",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        audio_output = gr.Textbox(
                            label="Transcription",
                            lines=15,
                            placeholder="Transcription will appear here..."
                        )
                
                gr.Markdown(
                    """
                    💡 **Note:** First transcription may take longer as the model loads
                    """
                )
                
                audio_button.click(
                    fn=transcribe_audio,
                    inputs=audio_input,
                    outputs=audio_output
                )
            
            # Tab 2: Image Analysis
            with gr.Tab("📸 Image Analysis"):
                gr.Markdown(
                    """
                    ### Analyze images and extract text using Claude Vision
                    Supports: PNG, JPG, JPEG, GIF, WEBP
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        image_input = gr.Image(
                            type="filepath",
                            label="Upload Image"
                        )
                        image_prompt = gr.Textbox(
                            label="Analysis Prompt (Optional)",
                            placeholder="e.g., 'Extract all text' or 'Describe this diagram'",
                            lines=3
                        )
                        image_button = gr.Button(
                            "📸 Analyze",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        image_output = gr.Textbox(
                            label="Analysis",
                            lines=15,
                            placeholder="Analysis will appear here..."
                        )
                
                gr.Markdown(
                    """
                    💡 **Tip:** Leave prompt empty for general analysis and text extraction
                    """
                )
                
                image_button.click(
                    fn=analyze_image,
                    inputs=[image_input, image_prompt],
                    outputs=image_output
                )
            
            # Tab 3: Meeting Minutes
            with gr.Tab("📝 Meeting Minutes"):
                gr.Markdown(
                    """
                    ### Generate structured meeting minutes from transcripts
                    """
                )
                
                with gr.Row():
                    with gr.Column():
                        transcript_input = gr.Textbox(
                            label="Meeting Transcript",
                            lines=15,
                            placeholder="Paste your meeting transcript here..."
                        )
                        minutes_button = gr.Button(
                            "📝 Generate Minutes",
                            variant="primary",
                            size="lg"
                        )
                    
                    with gr.Column():
                        minutes_output = gr.Textbox(
                            label="Meeting Minutes",
                            lines=15,
                            placeholder="Minutes will appear here..."
                        )
                
                gr.Markdown(
                    """
                    💡 **Tip:** Include speaker names and topics for better results
                    """
                )
                
                minutes_button.click(
                    fn=generate_meeting_minutes,
                    inputs=transcript_input,
                    outputs=minutes_output
                )
        
        gr.Markdown(
            """
            ---
            **Powered by:** Whisper AI (Audio) • Claude (Vision & Language) • Faster-Whisper
            """
        )
    
    return demo


def launch_app(
    host: str = None,
    port: int = None,
    share: bool = False
):
    """
    Launch the web application.
    
    Args:
        host: Server host (default: from settings)
        port: Server port (default: from settings)
        share: Whether to create a public link
    """
    host = host or settings.SERVER_HOST
    port = port or settings.SERVER_PORT
    
    print("\n" + "=" * 60)
    print("🚀 AI Content Processor Web Application")
    print("=" * 60)
    print(f"\n🌐 Server: http://{host}:{port}")
    print("⚠️  First use may be slower (model loading)")
    print("\nPress Ctrl+C to stop\n")
    
    demo = create_interface()
    
    demo.launch(
        server_name=host,
        server_port=port,
        share=share,
        quiet=False,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="purple")
    )


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        launch_app()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
