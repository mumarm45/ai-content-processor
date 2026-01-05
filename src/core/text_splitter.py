class Splitter:
    def __init__(self):
        pass
    
    def chunk_transcript(processed_transcript, chunk_size=200, chunk_overlap=20):
        try:
            # Try new LangChain import path first (v0.1.0+)
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError:
            try:
                # Fall back to old import path
                from langchain.text_splitter import RecursiveCharacterTextSplitter
            except ImportError:
                raise ImportError(
                    "Could not import RecursiveCharacterTextSplitter. "
                    "Please install: pip install langchain-text-splitters"
                )
        
        # Initialize the RecursiveCharacterTextSplitter with specified chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        # Split the transcript into chunks
        chunks = text_splitter.split_text(processed_transcript)
        return chunks
