# 🎙️📸📝 AI Content Processor

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-beta-yellow)

A powerful AI-powered application that processes audio, images, and text using state-of-the-art AI models. Built with Anthropic's Claude, Faster-Whisper, and Gradio.

## ✨ Features

### 🎙️ Audio Transcription
- Transcribe audio files to text using OpenAI's Whisper model
- Support for multiple audio formats: WAV, MP3, M4A, FLAC, OGG, and more
- Fast processing with faster-whisper implementation
- Configurable model sizes for speed vs. accuracy trade-offs

### 📸 Image Analysis
- Extract text and information from images using Claude Vision
- Support for multiple image formats: PNG, JPG, JPEG, GIF, WEBP
- Custom prompts for specific analysis needs
- Intelligent image processing with Claude's multimodal capabilities

### 📝 Document Processing
- Generate structured meeting minutes from transcripts
- AI-powered text analysis and summarization
- Professional formatting with key points, action items, and decisions

### 📝 Webpage Q&A
- Generate structured meeting minutes from transcripts
- AI-powered text analysis and summarization
- Professional formatting with key points, action items, and decisions

### 📊 Nutrition Analysis
- Analyze food items in images
- Provide detailed nutritional information
- Calorie counting and macronutrient breakdown

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-content-processor
   ```

2. **Create and activate virtual environment**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Or using venv
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv pip install -e .

   # Or using pip
   pip install -e .
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

### Configuration

Edit your `.env` file with your settings:

```env
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Model configuration
ANTHROPIC_MODEL_ID=claude-3-5-sonnet-20241022
TEMPERATURE=0.7
MAX_TOKENS=1024

# Optional: Audio settings
WHISPER_MODEL=tiny.en  # Options: tiny.en, base.en, small.en, medium.en, large-v3
WHISPER_DEVICE=cpu     # Options: cpu, cuda, mps
WHISPER_COMPUTE_TYPE=int8

# Optional: Server settings
SERVER_HOST=0.0.0.0
SERVER_PORT=5500
```

## 🎯 Usage

### Web Interface

Start the web application:

```bash
python src/web/app.py
```
Then open your browser to `http://localhost:5500`
or
```bash
python src/web/api.py
```
Then open your browser to `http://localhost:5400/api`

The interface provides four main features:
- **Audio Transcription**: Upload audio files and get instant transcriptions
- **Image Analysis**: Upload images for text extraction and analysis
- **Meeting Minutes**: Paste transcripts to generate structured minutes
- **Nutrition Analysis**: Upload food images to get nutritional information
- **Webpage Q&A**: Upload webpages to generate structured minutes

### First Run

⚠️ **Note**: The first time you use audio transcription, the Whisper model will be downloaded automatically. This may take a few minutes depending on your internet connection and chosen model size.

## 📦 Project Structure

```
ai-content-processor/
├── src/
│   ├── config/          # Configuration and settings
│   ├── core/            # Core business logic
│   ├── services/        # AI services (Audio, Image, Document, Nutrition)
│   └── web/             # Gradio web interface, Flask API
├── scripts/             # Utility scripts
├── tests/               # Test files
├── data/                # Data files (gitignored)
├── .env.example         # Example environment variables
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # This file
```

## 🔧 Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Code formatting

```bash
# Format with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/
```

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'ai_processor'**
```bash
# Reinstall the package in editable mode
pip install -e .
```

**2. OpenMP Library Conflict**
The application automatically handles OpenMP conflicts by setting `KMP_DUPLICATE_LIB_OK=TRUE`. If you encounter issues, this is already handled in the code.

**3. First transcription is slow**
This is normal! The Whisper model needs to be downloaded and loaded on first use. Subsequent transcriptions will be much faster.

**4. CUDA/GPU Issues**
If you want to use GPU acceleration:
- Set `WHISPER_DEVICE=cuda` in your `.env` file
- Ensure you have CUDA-compatible PyTorch installed
- For Apple Silicon: use `WHISPER_DEVICE=mps`

**5. Gradio compatibility**
This project uses Gradio 6.2.0+. The code has been updated to be compatible with the latest Gradio API changes.

## 📋 Requirements

### Core Dependencies
- **anthropic** (>=0.40.0): Claude AI API
- **faster-whisper** (1.0.3): Audio transcription
- **gradio** (>=5.0.0): Web interface
- **langchain** (>=0.3.0): LLM orchestration
- **pillow** (>=10.0.0): Image processing
- **torch** (>=2.2.0): ML framework
- **chromadb** (>=0.5.0): Vector database
- **python-dotenv** (>=1.0.0): Environment variables
- **sentence-transformers** (>=2.2.2): Text embedding
- **huggingface-hub** (>=0.33.5): HuggingFace integration

## 🌟 Whisper Model Sizes

Choose based on your needs:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny.en | ~75MB | ⚡⚡⚡⚡ | ⭐⭐ | Quick tests, demos |
| base.en | ~150MB | ⚡⚡⚡ | ⭐⭐⭐ | General use |
| small.en | ~500MB | ⚡⚡ | ⭐⭐⭐⭐ | Recommended |
| medium.en | ~1.5GB | ⚡ | ⭐⭐⭐⭐⭐ | High accuracy |
| large-v3 | ~3GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Muhammad Omar Muneer**
- Email: mumarm45@gmail.com

## 🙏 Acknowledgments

- **Anthropic** for Claude AI
- **OpenAI** for Whisper
- **Systran** for faster-whisper implementation
- **Gradio** for the amazing web interface framework
- **LangChain** for LLM orchestration tools

## 📚 Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Faster-Whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [Gradio Documentation](https://www.gradio.app/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://www.trychroma.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [HuggingFace Documentation](https://huggingface.co/)
- [SentenceTransformers Documentation](https://www.sbert.net/)

---

**Made with ❤️ using Anthropic, Whisper, HuggingFace, LangChain, ChromaDB, Flask, Python-dotenv, Gradio**




Feel free to explore the code, experiment with different models, and contribute to make this project even better!

Happy coding and learning! 🚀