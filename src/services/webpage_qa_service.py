"""
Webpage Q&A Service with Vector Database.

Uses existing embedding, text_splitter, and chroma_db modules from the project.
"""

import logging
import uuid
from typing import List, Dict, Optional
from datetime import datetime

from core.llm_client import LLMClient
from core.embedding import setup_embedding_model
from core.text_splitter import Splitter
from core.chroma_db import ChromsDBService

logger = logging.getLogger(__name__)


class WebpageQAServiceError(Exception):
    """Base exception for webpage Q&A service errors."""
    pass


class WebpageQAService:
    """
    Service for webpage content Q&A with vector database.
    Uses existing HuggingFace embeddings, text splitter, and ChromaDB from core modules.
    
    Example:
        >>> service = WebpageQAService()
        >>> session_id = service.store_webpage_content(title, url, content)
        >>> answer = service.ask_question(session_id, "What is this page about?")
    """
    
    def __init__(
        self, 
        llm_client: Optional[LLMClient] = None,
        embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """
        Initialize the webpage Q&A service.
        
        Args:
            llm_client: Optional LLM client instance
            embedding_model_name: HuggingFace model for embeddings
            chunk_size: Default chunk size for text splitting
            chunk_overlap: Default overlap between chunks
        """
        self.llm_client = llm_client or LLMClient(temperature=0.3)
        
        # Use existing embedding setup from core.embedding
        logger.info(f"Loading embedding model: {embedding_model_name}")
        self.embedding_model = setup_embedding_model(embedding_model_name)
        logger.info(f"✅ Embedding model loaded")
        
        # Store chunking parameters
        self.default_chunk_size = chunk_size
        self.default_chunk_overlap = chunk_overlap
        
        # Use existing ChromaDB service from core.chroma_db
        chromadb_service = ChromsDBService()
        
        # Get the ChromaDB client (it's an attribute, not a method call)
        self.chroma_client = chromadb_service.chromadb_client
        
        # Create or get collection using the service method
        self.collection = chromadb_service.get_or_create_collection(
            name="webpage_content",
            metadata={"description": "Webpage content for Q&A"}
        )
        
        # Store active sessions
        self.sessions: Dict[str, Dict] = {}
        
        logger.info("Initialized WebpageQAService with existing core modules")
    
    def _chunk_text(
        self, 
        text: str, 
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> List[str]:
        """
        Split text into chunks using existing Splitter from core.text_splitter.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk (uses default if None)
            chunk_overlap: Overlap between chunks (uses default if None)
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or self.default_chunk_size
        chunk_overlap = chunk_overlap or self.default_chunk_overlap
        
        # Use existing Splitter class
        chunks = Splitter.chunk_transcript(
            text, 
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        logger.info(f"✂️ Split text into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
        return chunks
    
    def _create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings using existing HuggingFace model from core.embedding.
        
        Args:
            texts: List of text chunks
            
        Returns:
            List of embedding vectors
        """
        logger.info(f"🔢 Creating embeddings for {len(texts)} chunks...")
        
        # Use the HuggingFaceEmbeddings model to embed documents
        embeddings = self.embedding_model.embed_documents(texts)
        
        logger.info(f"✅ Created {len(embeddings)} embeddings")
        return embeddings
    
    def store_webpage_content(
        self,
        title: str,
        url: str,
        content: str,
        metadata: Optional[Dict] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None
    ) -> str:
        """
        Store webpage content in vector database.
        All text should be combined into one string before calling this.
        
        Args:
            title: Page title
            url: Page URL
            content: Full page content (all text combined into one string)
            metadata: Optional additional metadata
            chunk_size: Size of each chunk (uses default if None)
            chunk_overlap: Overlap between chunks (uses default if None)
            
        Returns:
            Session ID for querying
            
        Raises:
            WebpageQAServiceError: If storage fails
        """
        try:
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            logger.info(f"📄 Storing webpage: {title}")
            logger.info(f"📊 Content length: {len(content)} characters")
            
            # Content should already be combined from frontend
            combined_text = content.strip()
            
            if not combined_text:
                raise WebpageQAServiceError("Content is empty")
            
            # Chunk the combined text using existing text_splitter
            chunks = self._chunk_text(
                combined_text, 
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            if not chunks:
                raise WebpageQAServiceError("No chunks created from content")
            
            logger.info(f"✂️ Created {len(chunks)} chunks from combined text")
            
            # Create embeddings using existing embedding model
            embeddings = self._create_embeddings(chunks)
            
            # Prepare metadata for each chunk
            chunk_metadata = []
            ids = []
            
            for i in range(len(chunks)):
                chunk_meta = {
                    "session_id": session_id,
                    "title": title,
                    "url": url,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "stored_at": datetime.now().isoformat()
                }
                
                # Add custom metadata
                if metadata:
                    chunk_meta.update(metadata)
                
                chunk_metadata.append(chunk_meta)
                ids.append(f"{session_id}_{i}")
            
            # Store in ChromaDB with embeddings from HuggingFace
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=chunk_metadata,
                ids=ids
            )
            
            # Store session info
            self.sessions[session_id] = {
                "title": title,
                "url": url,
                "chunks": len(chunks),
                "content_length": len(combined_text),
                "chunk_size": chunk_size or self.default_chunk_size,
                "chunk_overlap": chunk_overlap or self.default_chunk_overlap,
                "created_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            logger.info(f"✅ Stored session: {session_id}")
            logger.info(f"   - Chunks: {len(chunks)}")
            logger.info(f"   - Total content: {len(combined_text)} chars")
            
            return session_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store content: {e}", exc_info=True)
            raise WebpageQAServiceError(f"Storage failed: {e}") from e
    
    def ask_question(
        self,
        session_id: str,
        question: str,
        n_results: int = 3
    ) -> str:
        """
        Ask a question about stored webpage content.
        Uses HuggingFace embeddings for semantic search.
        
        Args:
            session_id: Session ID from store_webpage_content
            question: User's question
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            Answer to the question
            
        Raises:
            WebpageQAServiceError: If query fails
        """
        if session_id not in self.sessions:
            raise WebpageQAServiceError(f"Session not found: {session_id}")
        
        try:
            logger.info(f"❓ Question for session {session_id}: {question}")
            
            # Create embedding for the question using existing model
            question_embedding = self.embedding_model.embed_query(question)
            
            # Query similar chunks using the question embedding
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=n_results,
                where={"session_id": session_id}
            )
            
            if not results['documents'] or not results['documents'][0]:
                return "I couldn't find relevant information to answer your question."
            
            # Get relevant chunks
            relevant_chunks = results['documents'][0]
            
            logger.info(f"📚 Found {len(relevant_chunks)} relevant chunks")
            
            # Build context from relevant chunks
            context = "\n\n".join(relevant_chunks)
            
            # Get session info
            session_info = self.sessions[session_id]
            
            # Create prompt for LLM
            prompt = f"""You are a helpful AI assistant answering questions about a webpage.

Webpage Information:
- Title: {session_info['title']}
- URL: {session_info['url']}

Relevant Content from the webpage:
{context}

User Question: {question}

Please provide a clear, accurate answer based on the content above. If the content doesn't contain enough information to answer the question, say so honestly. Do not make up information.

Answer:"""
            
            # Get answer from LLM
            response = self.llm_client.invoke(prompt)
            
            if hasattr(response, 'content'):
                answer = response.content
            else:
                answer = str(response)
            
            logger.info(f"✅ Generated answer: {len(answer)} characters")
            
            return answer
            
        except Exception as e:
            logger.error(f"❌ Question answering failed: {e}", exc_info=True)
            raise WebpageQAServiceError(f"Query failed: {e}") from e
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Get information about a stored session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session information or None if not found
        """
        return self.sessions.get(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its stored content.
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if session_id not in self.sessions:
            return False
        
        try:
            # Delete from ChromaDB
            self.collection.delete(
                where={"session_id": session_id}
            )
            
            # Remove from sessions
            del self.sessions[session_id]
            
            logger.info(f"🗑️ Deleted session: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete session: {e}")
            return False
    
    def list_sessions(self) -> List[Dict]:
        """
        List all active sessions.
        
        Returns:
            List of session information
        """
        return [
            {"session_id": sid, **info}
            for sid, info in self.sessions.items()
        ]


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Sample content - all text combined into one
    sample_content = """
    The Python programming language is a high-level, interpreted language 
    known for its simplicity and readability. Created by Guido van Rossum 
    and first released in 1991, Python has become one of the most popular 
    programming languages in the world.
    
    Python is widely used in web development, data science, machine learning, 
    automation, and scientific computing. Its extensive standard library and 
    vibrant ecosystem of third-party packages make it suitable for a wide 
    range of applications.
    
    Key features of Python include dynamic typing, automatic memory management, 
    and support for multiple programming paradigms including procedural, 
    object-oriented, and functional programming.
    """
    
    print("=" * 60)
    print("Webpage Q&A Service Demo - Using Existing Core Modules")
    print("=" * 60)
    
    try:
        # Initialize service
        print("\n🔄 Initializing service with existing modules...")
        service = WebpageQAService()
        
        print("\n📄 Storing sample webpage content...")
        session_id = service.store_webpage_content(
            title="Python Programming Guide",
            url="https://example.com/python-guide",
            content=sample_content,
            chunk_size=500,
            chunk_overlap=100
        )
        
        print(f"\n✅ Session ID: {session_id}")
        
        questions = [
            "Who created Python?",
            "What is Python used for?",
            "When was Python first released?"
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            answer = service.ask_question(session_id, question)
            print(f"💬 Answer: {answer}")
        
    except WebpageQAServiceError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
