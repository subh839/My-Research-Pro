import unittest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock
import chromadb
import numpy as np

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from free_ai_client import FreeAIClient
from free_search_client import FreeSearchClient
from chroma_manager import ChromaManager, initialize_sample_data
from free_contextual_agent import FreeContextualAgent

class TestFreeAIClient(unittest.TestCase):
    """Test cases for FreeAIClient"""
    
    def setUp(self):
        self.ai_client = FreeAIClient()
    
    def test_initialization(self):
        """Test AI client initialization"""
        self.assertIsNotNone(self.ai_client)
        self.assertIn(self.ai_client.use_api, [True, False])
    
    def test_analyze_intent_basic(self):
        """Test basic intent analysis"""
        question = "What are the latest advancements in AI?"
        result = self.ai_client.analyze_intent(question)
        
        self.assertIsInstance(result, str)
        # Should return JSON or mock response
        self.assertTrue(len(result) > 0)
    
    def test_analyze_intent_with_keywords(self):
        """Test intent analysis with specific keywords"""
        # Test web-focused question
        web_question = "Latest news about quantum computing"
        web_result = self.ai_client.analyze_intent(web_question)
        self.assertIn('needs_web', web_result.lower())
        
        # Test internal-focused question  
        internal_question = "Our internal research on batteries"
        internal_result = self.ai_client.analyze_intent(internal_question)
        self.assertIn('needs_internal', internal_result.lower())
    
    def test_synthesize_answer(self):
        """Test answer synthesis with mock data"""
        question = "Test question"
        web_data = "Mock web data about technology"
        internal_data = "Mock internal research documents"
        
        result = self.ai_client.synthesize_answer(question, web_data, internal_data)
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn(question, result or '')
    
    def test_synthesize_with_empty_data(self):
        """Test synthesis with empty data"""
        question = "Test question"
        result = self.ai_client.synthesize_answer(question, "", "")
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

class TestFreeSearchClient(unittest.TestCase):
    """Test cases for FreeSearchClient"""
    
    def setUp(self):
        self.search_client = FreeSearchClient()
    
    def test_initialization(self):
        """Test search client initialization"""
        self.assertIsNotNone(self.search_client)
        self.assertTrue(hasattr(self.search_client, 'serper_key'))
    
    def test_query_basic(self):
        """Test basic query functionality"""
        query = "solid-state batteries"
        result = self.search_client.query(query)
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn('solid-state', result.lower() or '')
    
    def test_mock_search_coverage(self):
        """Test that mock search covers various topics"""
        test_queries = [
            "solid-state batteries",
            "AI regulation", 
            "renewable energy",
            "quantum computing",
            "unknown topic test"
        ]
        
        for query in test_queries:
            result = self.search_client.query(query)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0, f"Empty result for query: {query}")
    
    @patch('free_search_client.FreeSearchClient.search_serper')
    def test_serper_fallback(self, mock_serper):
        """Test Serper API fallback to mock data"""
        mock_serper.return_value = "Mock Serper results"
        
        # Even when Serper is called, it should return data
        result = self.search_client.query("test query")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

class TestChromaManager(unittest.TestCase):
    """Test cases for ChromaManager"""
    
    def setUp(self):
        # Use in-memory ChromaDB for testing
        self.chroma_manager = ChromaManager()
    
    def test_initialization(self):
        """Test ChromaDB manager initialization"""
        self.assertIsNotNone(self.chroma_manager)
        self.assertIsNotNone(self.chroma_manager.client)
        self.assertIsNotNone(self.chroma_manager.collection)
    
    def test_add_documents(self):
        """Test adding documents to ChromaDB"""
        test_documents = [
            "This is a test document about artificial intelligence.",
            "Another test document discussing machine learning algorithms."
        ]
        test_metadata = [
            {"source": "test", "type": "research"},
            {"source": "test", "type": "technical"}
        ]
        
        # Count before adding
        initial_count = self.chroma_manager.get_collection_stats()
        
        # Add documents
        self.chroma_manager.add_documents(test_documents, test_metadata)
        
        # Count after adding
        final_count = self.chroma_manager.get_collection_stats()
        self.assertEqual(final_count, initial_count + len(test_documents))
    
    def test_hybrid_search(self):
        """Test hybrid search functionality"""
        query = "artificial intelligence"
        results = self.chroma_manager.hybrid_search(query)
        
        self.assertIsInstance(results, list)
        # Should return list of dictionaries
        if len(results) > 0:
            first_result = results[0]
            self.assertIn('content', first_result)
            self.assertIn('metadata', first_result)
    
    def test_empty_search(self):
        """Test search with no results"""
        query = "completely unrelated topic that shouldn't match anything"
        results = self.chroma_manager.hybrid_search(query)
        
        self.assertIsInstance(results, list)
        # Could be empty or have some results
    
    def test_collection_stats(self):
        """Test collection statistics"""
        stats = self.chroma_manager.get_collection_stats()
        self.assertIsInstance(stats, int)
        self.assertGreaterEqual(stats, 0)

class TestFreeContextualAgent(unittest.TestCase):
    """Test cases for FreeContextualAgent"""
    
    def setUp(self):
        self.agent = FreeContextualAgent()
    
    def test_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.searcher)
        self.assertIsNotNone(self.agent.ai)
        self.assertIsNotNone(self.agent.chroma)
    
    def test_process_query_basic(self):
        """Test basic query processing"""
        question = "What is AI?"
        result = self.agent.process_query(question)
        
        self.assertIsInstance(result, dict)
        self.assertIn('answer', result)
        self.assertIn('sources_used', result)
        self.assertIn('intent_analysis', result)
        
        self.assertIsInstance(result['answer'], str)
        self.assertIsInstance(result['sources_used'], dict)
        self.assertIsInstance(result['intent_analysis'], dict)
    
    def test_process_query_complex(self):
        """Test complex query processing"""
        complex_questions = [
            "Compare our internal battery research with recent market developments",
            "What AI regulations affect our company and what's our compliance status?",
            "Latest renewable energy trends and our current projects"
        ]
        
        for question in complex_questions:
            result = self.agent.process_query(question)
            
            self.assertIsInstance(result, dict)
            self.assertTrue(len(result['answer']) > 0)
            self.assertIn('web', result['sources_used'])
            self.assertIn('internal', result['sources_used'])
    
    def test_agent_info(self):
        """Test agent information retrieval"""
        info = self.agent.get_agent_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('has_gemini_api', info)
        self.assertIn('knowledge_base_docs', info)
        self.assertIn('search_capability', info)
        
        self.assertIsInstance(info['has_gemini_api'], bool)
        self.assertIsInstance(info['knowledge_base_docs'], int)
        self.assertIsInstance(info['search_capability'], str)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_end_to_end_workflow(self):
        """Test complete research workflow"""
        agent = FreeContextualAgent()
        
        test_questions = [
            "Latest developments in battery technology",
            "Our internal AI research projects",
            "Renewable energy market analysis"
        ]
        
        for question in test_questions:
            with self.subTest(question=question):
                result = agent.process_query(question)
                
                # Verify result structure
                self.assertIsInstance(result, dict)
                self.assertIn('answer', result)
                self.assertIn('sources_used', result)
                
                # Answer should be substantial
                self.assertGreater(len(result['answer']), 100)
                
                # Sources should be properly indicated
                sources = result['sources_used']
                self.assertIn('web', sources)
                self.assertIn('internal', sources)
                self.assertIsInstance(sources['web'], bool)
                self.assertIsInstance(sources['internal'], bool)

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    @patch('free_ai_client.FreeAIClient.analyze_intent')
    def test_agent_with_ai_failure(self, mock_analyze):
        """Test agent behavior when AI service fails"""
        mock_analyze.side_effect = Exception("AI service unavailable")
        
        agent = FreeContextualAgent()
        result = agent.process_query("test question")
        
        # Should still return a result structure
        self.assertIsInstance(result, dict)
        self.assertIn('answer', result)
    
    @patch('free_search_client.FreeSearchClient.query')
    def test_agent_with_search_failure(self, mock_search):
        """Test agent behavior when search fails"""
        mock_search.side_effect = Exception("Search service down")
        
        agent = FreeContextualAgent()
        result = agent.process_query("test question")
        
        # Should handle search failure gracefully
        self.assertIsInstance(result, dict)
        self.assertIn('sources_used', result)

def run_performance_tests():
    """Performance testing utilities"""
    import time
    
    def test_response_time():
        """Test average response time"""
        agent = FreeContextualAgent()
        test_questions = [
            "Simple question",
            "Complex research query", 
            "Technical analysis request"
        ]
        
        times = []
        for question in test_questions:
            start_time = time.time()
            result = agent.process_query(question)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        print(f"Average response time: {avg_time:.2f} seconds")
        return avg_time
    
    return test_response_time()

if __name__ == '__main__':
    # Run unit tests
    print("🧪 Running Unit Tests...")
    unittest.main(verbosity=2)
    
    # Run performance tests
    print("\n⚡ Running Performance Tests...")
    avg_time = run_performance_tests()
    print(f"✅ Performance test completed. Average time: {avg_time:.2f}s")