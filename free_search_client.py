import os
import requests
import json
import random
from dotenv import load_dotenv

load_dotenv()

class FreeSearchClient:
    def __init__(self):
        self.serper_key = os.getenv('SERPER_API_KEY')
        self.use_serper = self.serper_key and self.serper_key != "your_free_serper_key_here"
        
    def search_serper(self, query):
        """Enhanced Serper API with better error handling"""
        if not self.use_serper:
            return self.enhanced_mock_search(query)
        
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query, 
            "num": 7,
            "gl": "us",
            "hl": "en"
        })
        headers = {
            'X-API-KEY': self.serper_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            results = response.json()
            
            return self.format_serper_results(results, query)
            
        except requests.exceptions.Timeout:
            return self.enhanced_mock_search(query, "Request timeout - using enhanced mock data")
        except Exception as e:
            return self.enhanced_mock_search(query, f"API error: {str(e)} - using enhanced mock data")
    
    def format_serper_results(self, results, original_query):
        """Better formatting for search results"""
        formatted = "## 🌐 Latest Web Research\n\n"
        
        if 'organic' in results and results['organic']:
            for i, item in enumerate(results['organic'][:5], 1):
                formatted += f"### 📰 {item.get('title', 'No title')}\n"
                formatted += f"**Summary:** {item.get('snippet', 'No description available')}\n\n"
                if 'link' in item:
                    formatted += f"🔗 **Source:** [{item['link'][:50]}...]({item['link']})\n"
                formatted += "---\n\n"
            
            # Add search stats
            formatted += f"*Found {len(results['organic'])} results for '{original_query}'*\n"
        else:
            formatted += "No web results found. Try different keywords or check your query.\n"
        
        return formatted
    
    def enhanced_mock_search(self, query, reason="using enhanced mock database"):
        """Massively improved mock search with more topics and better data"""
        
        # Expanded mock database
        mock_database = {
            "solid-state batteries": {
                "title": "Solid-State Battery Breakthroughs 2024",
                "results": [
                    {
                        "title": "QuantumScape Achieves 900 Wh/L Energy Density",
                        "snippet": "QuantumScape announces commercial-scale solid-state batteries achieving 900 Wh/L energy density, enabling 500+ mile EV ranges and 10-minute fast charging. Production planned for 2025.",
                        "source": "https://quantumscape.com/breakthrough"
                    },
                    {
                        "title": "Toyota Solid-State Production Timeline",
                        "snippet": "Toyota confirms 2027 launch for vehicles with solid-state batteries, claiming 750+ mile range and unprecedented safety features. Manufacturing partnership with Panasonic announced.",
                        "source": "https://toyota.com/innovation"
                    },
                    {
                        "title": "MIT New Electrolyte Material Research",
                        "snippet": "MIT researchers develop new ceramic electrolyte that enables 2000+ cycle life while maintaining high conductivity. Patent pending for the novel material composition.",
                        "source": "https://mit.edu/battery-research"
                    },
                    {
                        "title": "Solid-State Battery Cost Reduction Roadmap",
                        "snippet": "Industry analysis predicts 40% cost reduction by 2026 through improved manufacturing processes and material innovations. DOE grants $200M for domestic production.",
                        "source": "https://energy.gov/battery-funding"
                    }
                ]
            },
            "ai regulation": {
                "title": "Global AI Regulation Updates",
                "results": [
                    {
                        "title": "EU AI Act Final Implementation",
                        "snippet": "European Parliament approves final AI Act text with strict requirements for high-risk AI systems. Compliance deadline set for 2025 with significant penalties for violations.",
                        "source": "https://europa.eu/ai-act"
                    },
                    {
                        "title": "US Executive Order on AI Safety",
                        "snippet": "White House issues comprehensive AI safety executive order requiring testing for powerful models and establishing new security standards. $1.6B allocated for AI research.",
                        "source": "https://whitehouse.gov/ai-order"
                    },
                    {
                        "title": "China AI Governance Framework",
                        "snippet": "China releases detailed AI governance rules focusing on generative AI, data security, and algorithmic transparency. Special emphasis on content management and oversight.",
                        "source": "https://gov.cn/ai-regulation"
                    },
                    {
                        "title": "UK AI Safety Summit Outcomes",
                        "snippet": "International AI Safety Summit concludes with 28 countries signing declaration on cooperative AI safety testing. New global research network established.",
                        "source": "https://gov.uk/ai-safety"
                    }
                ]
            },
            "renewable energy": {
                "title": "Renewable Energy Innovations 2024",
                "results": [
                    {
                        "title": "Perovskite Solar Cells Hit 47% Efficiency",
                        "snippet": "New tandem perovskite-silicon solar cells achieve record 47% efficiency in lab conditions, potentially cutting solar energy costs by 60% within 3 years.",
                        "source": "https://solarresearch.org/breakthrough"
                    },
                    {
                        "title": "Offshore Wind Capacity Tripling Plans",
                        "snippet": "Global offshore wind capacity set to triple by 2030 with $300B in new investments. Major projects announced in North Sea and US East Coast.",
                        "source": "https://energynews.com/wind-expansion"
                    },
                    {
                        "title": "Green Hydrogen Cost Breakthrough",
                        "snippet": "New electrolyzer technology reduces green hydrogen production costs to $2/kg, making it competitive with fossil fuels. DOE announces $7B funding for regional hubs.",
                        "source": "https://hydrogen-future.com/cost-reduction"
                    }
                ]
            },
            "quantum computing": {
                "title": "Quantum Computing Advances",
                "results": [
                    {
                        "title": "IBM Announces 1000+ Qubit Processor",
                        "snippet": "IBM unveils 1121-qubit Condor processor, marking milestone in quantum computing scale. Demonstrates quantum advantage in specific optimization problems.",
                        "source": "https://ibm.com/quantum-breakthrough"
                    },
                    {
                        "title": "Quantum Error Correction Milestone",
                        "snippet": "Google achieves fault-tolerant quantum computation with 99.9% gate fidelity. Breakthrough enables longer quantum calculations with reduced errors.",
                        "source": "https://research.google/quantum"
                    }
                ]
            }
        }
        
        # Find best matching topic
        best_match = None
        best_score = 0
        
        for topic, data in mock_database.items():
            score = sum(1 for word in topic.split() if word in query.lower())
            if score > best_score:
                best_score = score
                best_match = topic
        
        if best_match:
            data = mock_database[best_match]
            formatted = f"## 🌐 {data['title']}\n\n"
            formatted += f"*🔍 Mock data for '{query}' - {reason}*\n\n"
            
            for i, result in enumerate(data['results'], 1):
                formatted += f"### 📰 {result['title']}\n"
                formatted += f"**Summary:** {result['snippet']}\n\n"
                formatted += f"🔗 **Source:** {result['source']}\n"
                formatted += "---\n\n"
            
            return formatted
        
        # Generic response for unknown topics
        return f"""## 🌐 Web Research: {query}

**🔍 Enhanced Mock Data - {reason}**

### 📰 Industry Analysis Report
**Summary:** Recent market analysis shows significant developments and growing investment in this sector. Multiple companies are reporting breakthroughs and new product announcements.

🔗 **Source:** https://industry-news.com/analysis

### 📰 Research Institution Findings  
**Summary:** Academic research continues to advance the fundamental understanding and practical applications in this field. Several patents have been filed recently.

🔗 **Source:** https://research-updates.edu/breakthroughs

### 📰 Government Policy Update
**Summary:** Regulatory frameworks are evolving to address new challenges and opportunities. Funding programs have been announced to support innovation.

🔗 **Source:** https://government.gov/policy-update

*💡 For real-time results, add a free Serper API key (100 searches/month)*"""

    def query(self, question):
        """Enhanced query with topic detection"""
        return self.search_serper(question)

# Test the enhanced search
if __name__ == "__main__":
    client = FreeSearchClient()
    test_queries = ["solid-state batteries", "quantum computing news", "unknown topic test"]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print('='*60)
        result = client.query(query)
        print(result)