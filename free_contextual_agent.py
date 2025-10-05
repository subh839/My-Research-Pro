import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Import other components
try:
    from free_search_client import FreeSearchClient
    from free_ai_client import FreeAIClient
    from chroma_manager import ChromaManager, initialize_sample_data
except ImportError as e:
    print(f"Import error: {e}")
    # Create dummy classes for testing
    class FreeSearchClient:
        def query(self, question):
            return f"Mock web results for: {question}"
    
    class FreeAIClient:
        def __init__(self):
            self.use_api = False
        def analyze_intent(self, question):
            return '{"needs_web": true, "needs_internal": true}'
        def synthesize_answer(self, question, web_data, internal_data):
            return f"Answer to: {question}\nWeb: {web_data[:100]}...\nInternal: {internal_data[:100]}..."
    
    class ChromaManager:
        def __init__(self):
            pass
        def hybrid_search(self, query):
            return [{"content": f"Mock internal doc about {query}", "metadata": {}}]
        def get_collection_stats(self):
            return 8

class FreeContextualAgent:
    def __init__(self):
        print("🔄 Initializing FreeContextualAgent...")
        self.searcher = FreeSearchClient()
        self.ai = FreeAIClient()
        self.chroma = ChromaManager()
        print("✅ FreeContextualAgent initialized successfully!")
    
    def parse_intent_analysis(self, analysis_text):
        """Parse intent analysis from AI response"""
        try:
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "needs_web": True,
            "needs_internal": True,
            "reasoning": "Default analysis",
            "web_query": analysis_text[:100],
            "internal_query": analysis_text[:100]
        }
    
    def process_query(self, user_question):
        """Main method to process user questions"""
        print(f"🔍 Processing: {user_question}")
        
        # Step 1: Analyze intent
        intent_analysis = self.ai.analyze_intent(user_question)
        intent = self.parse_intent_analysis(intent_analysis)
        
        # Step 2: Gather data
        web_data = ""
        internal_data = ""
        
        if intent.get('needs_web', True):
            web_query = intent.get('web_query', user_question)
            web_data = self.searcher.query(web_query)
        
        if intent.get('needs_internal', True):
            internal_query = intent.get('internal_query', user_question)
            internal_results = self.chroma.hybrid_search(internal_query)
            
            if internal_results:
                internal_data = "Internal Knowledge:\n"
                for i, result in enumerate(internal_results, 1):
                    internal_data += f"{i}. {result['content']}\n"
            else:
                internal_data = "No internal documents found."
        
        # Step 3: Synthesize answer
        final_answer = self.ai.synthesize_answer(user_question, web_data, internal_data)
        
        return {
            "answer": final_answer,
            "sources_used": {
                "web": intent.get('needs_web', False),
                "internal": intent.get('needs_internal', False)
            },
            "intent_analysis": intent
        }

    def get_agent_info(self):
        """Get information about the agent's capabilities"""
        return {
            "has_gemini_api": getattr(self.ai, 'use_api', False),
            "knowledge_base_docs": self.chroma.get_collection_stats(),
            "search_capability": "Mock Data"
        }

# Initialize sample data when module is imported
try:
    initialize_sample_data()
except:
    print("⚠️ Could not initialize sample data")