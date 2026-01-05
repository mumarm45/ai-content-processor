"""
Flask API for Chrome Extension integration.

Provides REST API endpoints for:
1. Storing webpage content
2. Q&A chatbot functionality
"""

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict

from services import WebpageQAService, WebpageQAServiceError

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Initialize service
qa_service = WebpageQAService()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'API is running',
        'service': 'Webpage Q&A API'
    })


@app.route('/api/webpage/store', methods=['POST'])
def store_webpage():
    """
    Store webpage content for Q&A.
    
    Expected JSON body:
    {
        "metadata": {
            "title": "Page Title",
            "url": "https://example.com",
            "wordCount": 1234,
            ...
        },
        "content": {
            "fullText": "Complete page content...",
            "headings": [...],
            "links": [...]
        }
    }
    
    Returns:
        JSON with session_id for Q&A
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        metadata = data.get('metadata', {})
        content = data.get('content', {})
        
        title = metadata.get('title', 'Untitled Page')
        url = metadata.get('url', '')
        
        # Combine all text into one - get fullText from content
        full_text = content.get('fullText', '')
        
        # Optionally, you can also combine headings and other text
        # But fullText already contains everything from the page
        combined_text = full_text.strip()
        
        if not combined_text:
            return jsonify({
                'success': False,
                'error': 'No content provided'
            }), 400
        
        logger.info(f"📝 Combined text length: {len(combined_text)} characters")
        
        logger.info(f"📄 Received webpage: {title}")
        logger.info(f"📊 Content length: {len(full_text)} characters")
        
        # Store in vector database with combined text
        session_id = qa_service.store_webpage_content(
            title=title,
            url=url,
            content=combined_text,  # All text combined into one
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'message': 'Content stored successfully',
            'data': {
                'session_id': session_id,
                'title': title,
                'url': url,
                'wordCount': metadata.get('wordCount', 0),
                'storedAt': qa_service.sessions[session_id]['created_at']
            }
        })
        
    except WebpageQAServiceError as e:
        logger.error(f"❌ Service error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/webpage/ask', methods=['POST'])
def ask_question():
    """
    Ask a question about stored webpage content.
    
    Expected JSON body:
    {
        "session_id": "uuid-here",
        "question": "What is this page about?"
    }
    
    Returns:
        JSON with answer
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        session_id = data.get('session_id')
        question = data.get('question')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'session_id is required'
            }), 400
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'question is required'
            }), 400
        
        logger.info(f"❓ Question for session {session_id}: {question}")
        
        # Get answer
        answer = qa_service.ask_question(session_id, question)
        
        # Get session info
        session_info = qa_service.get_session_info(session_id)
        
        return jsonify({
            'success': True,
            'data': {
                'answer': answer,
                'question': question,
                'session': {
                    'title': session_info['title'],
                    'url': session_info['url']
                }
            }
        })
        
    except WebpageQAServiceError as e:
        logger.error(f"❌ Service error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/webpage/sessions', methods=['GET'])
def list_sessions():
    """
    List all active sessions.
    
    Returns:
        JSON with list of sessions
    """
    try:
        sessions = qa_service.list_sessions()
        
        return jsonify({
            'success': True,
            'data': {
                'sessions': sessions,
                'count': len(sessions)
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Error listing sessions: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/webpage/session/<session_id>', methods=['DELETE'])
def delete_session(session_id: str):
    """
    Delete a session and its stored content.
    
    Args:
        session_id: Session ID to delete
        
    Returns:
        JSON with success status
    """
    try:
        deleted = qa_service.delete_session(session_id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Session deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
            
    except Exception as e:
        logger.error(f"❌ Error deleting session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def run_api_server(host: str = '0.0.0.0', port: int = 5400, debug: bool = False):
    """
    Run the Flask API server.
    
    Args:
        host: Server host
        port: Server port
        debug: Debug mode
    """
    print("\n" + "=" * 60)
    print("🚀 Webpage Q&A API Server")
    print("=" * 60)
    print(f"\n🌐 Server: http://{host}:{port}")
    print(f"📡 Store endpoint: http://{host}:{port}/api/webpage/store")
    print(f"💬 Q&A endpoint: http://{host}:{port}/api/webpage/ask")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        run_api_server(debug=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
