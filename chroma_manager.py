import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

class ChromaManager:
    def __init__(self):
        self.db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.collection = self.client.get_or_create_collection("knowledge_base")
        print("✅ ChromaDB initialized successfully!")
    
    def add_documents(self, documents, metadatas=None, ids=None):
        """Add documents to ChromaDB"""
        if not documents:
            return
        
        embeddings = self.embedder.encode(documents).tolist()
        
        if not ids:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas or [{}] * len(documents),
            ids=ids
        )
        print(f"✅ Added {len(documents)} documents to knowledge base")
    
    def search(self, query, n_results=5):
        """Enhanced search with more results"""
        query_embedding = self.embedder.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        return results
    
    def hybrid_search(self, query, n_results=5):
        """Enhanced hybrid search"""
        results = self.search(query, n_results)
        
        formatted_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                formatted_results.append({
                    'content': doc,
                    'metadata': metadata,
                    'score': 1.0
                })
        
        return formatted_results

    def get_collection_stats(self):
        """Get statistics about the knowledge base"""
        return self.collection.count()

# Expanded sample data with 25+ documents across multiple domains
def initialize_sample_data():
    manager = ChromaManager()
    
    # Expanded sample documents - 25 documents across multiple domains
    sample_docs = [
        # Technology & AI (8 documents)
        "Project Ares - Solid State Battery Research: Achieved 750 Wh/L energy density with 2000 cycle life at 80% capacity retention. Current manufacturing focus aims for 40% cost reduction through automated production lines.",
        
        "AI Ethics Committee Q2 2024 Report: Recommended implementing AI transparency protocols by Q3 2024. Identified 5 key compliance areas needing updates to meet EU AI Act requirements. Budget allocation: $2.5M for compliance infrastructure.",
        
        "Quantum Computing Initiative 2024: Established partnership with Quantum Research Institute. Current focus on developing 50-qubit quantum processors. Projected timeline: Prototype by Q4 2024, commercial deployment 2026.",
        
        "Cloud Infrastructure Migration: Completed 80% migration to multi-cloud architecture. Achieved 40% cost reduction and 99.95% uptime. Remaining workloads scheduled for Q3 2024 migration.",
        
        "Cybersecurity Framework Update: Implemented zero-trust architecture across all systems. Reduced security incidents by 65% year-over-year. Next phase: AI-powered threat detection deployment.",
        
        "Data Analytics Platform: Launched new real-time analytics platform processing 2TB daily. Customer adoption at 45% within first quarter. ROI projection: 3.2x within 18 months.",
        
        "IoT Integration Project: Deployed 10,000 IoT sensors across manufacturing facilities. Resulted in 25% operational efficiency improvement. Expansion planned for Q1 2025.",
        
        "Blockchain Supply Chain: Pilot program showing 30% reduction in supply chain disputes. Full implementation scheduled for 2025 across all logistics partners.",

        # Business & Strategy (6 documents)
        "Q3 2024 Financial Projections: Battery division shows 28% growth based on current research outcomes. Renewable energy projects contributed $4.7M revenue last quarter. Projected annual growth: 22%.",
        
        "Market Expansion Strategy Asia-Pacific: Entered 3 new markets with localized offerings. Current market share: 8%, target: 15% by 2025. Investment: $15M over 3 years.",
        
        "M&A Strategy Update: Identified 5 acquisition targets in AI and renewable energy sectors. Due diligence completed on 2 targets. Expected deal closure: Q4 2024.",
        
        "Customer Success Metrics Q2 2024: Overall satisfaction score: 94% (up from 88%). Key improvement areas: support response time (now under 2 hours), product documentation.",
        
        "Strategic Partnerships 2024: Formed 3 new technology partnerships. Joint development projects expected to generate $12M in additional revenue over 2 years.",
        
        "Sustainability Initiative Progress: Reduced carbon footprint by 35% year-over-year. On track to meet 2025 sustainability goals. Renewable energy usage: 65% of total consumption.",

        # Research & Development (6 documents)
        "Advanced Materials Research: Developed new graphene composite with 3x conductivity of traditional materials. Patent filed, commercial applications in battery and semiconductor industries.",
        
        "Machine Learning Optimization: New algorithm reduced training time by 60% while maintaining 99% accuracy. Deployed across all AI products, resulting in 25% cost savings.",
        
        "Renewable Energy Storage: Breakthrough in hydrogen storage technology achieving 80% efficiency. Pilot plant construction beginning Q3 2024.",
        
        "Biotech Convergence: Exploring AI applications in personalized medicine. Initial research shows 40% improvement in treatment prediction accuracy.",
        
        "Space Technology Division: Secured $8M contract for satellite communication technology. First prototype delivery scheduled for Q1 2025.",
        
        "Autonomous Systems Research: Developed new navigation algorithm with 99.9% accuracy in complex environments. Applications in robotics, drones, and autonomous vehicles.",

        # Operations & Compliance (5 documents)
        "Manufacturing Process Innovation: New solid-state battery manufacturing technique reduced production time by 45% and material waste by 35%. Patent pending, scaling to full production.",
        
        "Quality Assurance Framework: Implemented AI-powered quality control achieving 99.98% defect detection rate. Reduced warranty claims by 40%.",
        
        "Regulatory Compliance Status: 88% compliant with new international AI regulations. Compliance target: 95% by Q4 2024. Remaining gaps in data governance and algorithmic transparency.",
        
        "Supply Chain Optimization: Reduced logistics costs by 22% through route optimization and supplier consolidation. Improved delivery times by 35%.",
        
        "Talent Development Program: Launched AI skills certification program. 75% of technical staff completed advanced training. Hiring target: 200 new AI specialists in 2024."
    ]
    
    sample_metadata = [
        # Technology & AI metadata
        {"source": "internal", "type": "research", "project": "Ares", "department": "R&D", "domain": "battery", "confidence": "high"},
        {"source": "internal", "type": "policy", "department": "AI Ethics", "status": "approved", "domain": "ai", "priority": "high"},
        {"source": "internal", "type": "research", "project": "Quantum", "department": "Advanced Research", "domain": "quantum", "timeline": "2026"},
        {"source": "internal", "type": "infrastructure", "department": "IT", "status": "completed", "domain": "cloud", "impact": "high"},
        {"source": "internal", "type": "security", "department": "Cybersecurity", "status": "implemented", "domain": "security", "priority": "critical"},
        {"source": "internal", "type": "platform", "department": "Data Science", "status": "live", "domain": "analytics", "roi": "high"},
        {"source": "internal", "type": "iot", "department": "Manufacturing", "status": "deployed", "domain": "iot", "efficiency": "25%"},
        {"source": "internal", "type": "blockchain", "department": "Supply Chain", "status": "pilot", "domain": "blockchain", "potential": "high"},

        # Business & Strategy metadata
        {"source": "internal", "type": "financial", "quarter": "Q3", "department": "Finance", "domain": "finance", "confidence": "high"},
        {"source": "internal", "type": "strategy", "region": "APAC", "department": "Business Development", "domain": "expansion", "investment": "$15M"},
        {"source": "internal", "type": "strategy", "department": "M&A", "status": "active", "domain": "acquisition", "timeline": "Q4 2024"},
        {"source": "internal", "type": "metrics", "department": "Customer Success", "quarter": "Q2", "domain": "customer", "satisfaction": "94%"},
        {"source": "internal", "type": "partnerships", "department": "Business Development", "status": "active", "domain": "partnerships", "revenue": "$12M"},
        {"source": "internal", "type": "sustainability", "department": "Operations", "status": "ongoing", "domain": "sustainability", "reduction": "35%"},

        # Research & Development metadata
        {"source": "internal", "type": "research", "department": "Materials Science", "domain": "materials", "innovation": "breakthrough", "patent": "filed"},
        {"source": "internal", "type": "research", "department": "AI Research", "domain": "machine learning", "efficiency": "60%", "impact": "high"},
        {"source": "internal", "type": "research", "department": "Energy", "domain": "renewable", "efficiency": "80%", "timeline": "Q3 2024"},
        {"source": "internal", "type": "research", "department": "Biotech", "domain": "healthcare", "improvement": "40%", "application": "medicine"},
        {"source": "internal", "type": "research", "department": "Space Tech", "domain": "aerospace", "contract": "$8M", "timeline": "Q1 2025"},
        {"source": "internal", "type": "research", "department": "Autonomous Systems", "domain": "robotics", "accuracy": "99.9%", "applications": "multiple"},

        # Operations & Compliance metadata
        {"source": "internal", "type": "manufacturing", "department": "Production", "improvement": "45%", "domain": "operations", "status": "scaling"},
        {"source": "internal", "type": "quality", "department": "QA", "accuracy": "99.98%", "domain": "operations", "impact": "high"},
        {"source": "internal", "type": "compliance", "department": "Legal", "status": "88%", "domain": "regulatory", "target": "95%"},
        {"source": "internal", "type": "operations", "department": "Supply Chain", "savings": "22%", "domain": "logistics", "improvement": "35%"},
        {"source": "internal", "type": "hr", "department": "Talent", "completion": "75%", "domain": "workforce", "hiring": "200"}
    ]
    
    # Only add if collection is empty or small
    current_count = manager.get_collection_stats()
    if current_count < 20:  # Only add if we have less than 20 documents
        manager.add_documents(sample_docs, sample_metadata)
        print(f"✅ Expanded knowledge base loaded with {len(sample_docs)} internal documents")
        print("📊 Domains covered: Technology, Business, Research, Operations")
    else:
        print(f"ℹ️  Knowledge base already contains {current_count} documents")

# Enhanced document processor for adding custom documents
def add_custom_documents(file_paths):
    """Add custom documents to the knowledge base"""
    manager = ChromaManager()
    
    documents = []
    metadatas = []
    
    for file_path in file_paths:
        if os.path.exists(file_path):
            # Simple text file reading
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(content)
                    metadatas.append({
                        "source": "custom",
                        "filename": os.path.basename(file_path),
                        "type": "document",
                        "added_date": "2024-01-01"
                    })
    
    if documents:
        manager.add_documents(documents, metadatas)
        print(f"✅ Added {len(documents)} custom documents to knowledge base")

if __name__ == "__main__":
    initialize_sample_data()
    
    # Example: Add custom documents
    # add_custom_documents(['doc1.txt', 'doc2.txt'])