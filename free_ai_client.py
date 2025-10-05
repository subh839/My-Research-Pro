import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class FreeAIClient:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and api_key != "your_free_gemini_key_here":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_api = True
            print("✅ Using Google Gemini API (Free Tier)")
        else:
            self.use_api = False
            print("🔄 Using enhanced mock AI responses")
    
    def analyze_intent(self, user_question):
        """Enhanced intent analysis with better context understanding"""
        
        if self.use_api:
            try:
                prompt = f"""
                Analyze this research question in depth and determine the optimal information sources needed.
                
                QUESTION: "{user_question}"
                
                Consider these aspects:
                1. Time sensitivity - does it need recent/current information?
                2. Organizational context - does it mention "our", "internal", "company"?
                3. Technical depth - does it require specialized/internal knowledge?
                4. Comparative analysis - does it ask for comparisons?
                5. Action orientation - does it require recommendations?
                
                Return ONLY valid JSON:
                {{
                    "needs_web": boolean,
                    "needs_internal": boolean,
                    "confidence": "high/medium/low",
                    "reasoning": "detailed explanation",
                    "web_query": "optimized search query for web",
                    "internal_query": "optimized search query for internal docs",
                    "question_type": "technical/strategic/comparative/regulatory/trends",
                    "expected_sections": ["section1", "section2", ...]
                }}
                """
                response = self.model.generate_content(prompt)
                return self._clean_json_response(response.text)
            except Exception as e:
                print(f"❌ Gemini API error: {e}")
        
        return self._enhanced_mock_intent(user_question)
    
    def _clean_json_response(self, text):
        """Extract and clean JSON from AI response"""
        import re
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json_match.group()
        except:
            pass
        return self._enhanced_mock_intent(text)
    
    def _enhanced_mock_intent(self, user_question):
        """Improved mock intent analysis"""
        question_lower = user_question.lower()
        
        # Enhanced keyword detection
        web_keywords = ['latest', 'recent', 'news', 'current', 'update', '2024', 'new', 'breaking', 'today', 'trend', 'market']
        internal_keywords = ['our', 'internal', 'company', 'project', 'team', 'we', 'document', 'file', 'research', 'compliance']
        technical_keywords = ['technical', 'specifications', 'architecture', 'framework', 'methodology']
        comparative_keywords = ['compare', 'versus', 'vs', 'difference', 'similar', 'contrast', 'better than']
        
        needs_web = any(word in question_lower for word in web_keywords)
        needs_internal = any(word in question_lower for word in internal_keywords)
        is_technical = any(word in question_lower for word in technical_keywords)
        is_comparative = any(word in question_lower for word in comparative_keywords)
        
        # Smart defaults with context
        if not needs_web and not needs_internal:
            if is_comparative:
                needs_web = True
                needs_internal = True
            elif is_technical:
                needs_internal = True
            else:
                needs_web = True
        
        # Determine question type
        if is_comparative:
            question_type = "comparative"
            expected_sections = ["Comparison Matrix", "Strengths/Weaknesses", "Recommendations"]
        elif is_technical:
            question_type = "technical"
            expected_sections = ["Technical Specifications", "Implementation Details", "Technical Challenges"]
        elif needs_internal and not needs_web:
            question_type = "internal"
            expected_sections = ["Internal Status", "Current Projects", "Resource Allocation"]
        else:
            question_type = "strategic"
            expected_sections = ["Market Analysis", "Trends", "Strategic Recommendations"]
        
        return json.dumps({
            "needs_web": needs_web,
            "needs_internal": needs_internal,
            "confidence": "high",
            "reasoning": f"Web: {needs_web} (current info), Internal: {needs_internal} (org context), Type: {question_type}",
            "web_query": user_question,
            "internal_query": user_question,
            "question_type": question_type,
            "expected_sections": expected_sections
        }, indent=2)
    
    def synthesize_answer(self, user_question, web_data, internal_data):
        """Greatly enhanced answer synthesis with structured reporting"""
        
        if self.use_api:
            try:
                prompt = self._create_enhanced_research_prompt(user_question, web_data, internal_data)
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"❌ Gemini API synthesis error: {e}")
        
        return self._enhanced_research_report(user_question, web_data, internal_data)
    
    def _create_enhanced_research_prompt(self, user_question, web_data, internal_data):
        """Create sophisticated prompt for professional research reports"""
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        return f"""
        You are a senior research analyst at a top consulting firm. Create a comprehensive, professional research report.

        RESEARCH REQUEST: "{user_question}"
        REPORT DATE: {current_date}

        ====================
        EXTERNAL MARKET INTELLIGENCE:
        ====================
        {web_data if web_data else "No external market data available"}

        ====================
        INTERNAL ORGANIZATIONAL KNOWLEDGE:
        ====================
        {internal_data if internal_data else "No internal organizational data available"}

        CREATE A PROFESSIONAL RESEARCH REPORT WITH THESE SECTIONS:

        # Executive Summary
        - Key findings and recommendations (3-4 bullet points)
        - Immediate actionable insights

        ## 1. Market Overview & Current Landscape
        - Current market state and key players
        - Recent developments and trends
        - Market size and growth projections

        ## 2. Technical Analysis
        - Technical specifications and capabilities
        - Innovation trends and breakthroughs
        - Technical challenges and limitations

        ## 3. Competitive Landscape
        - Key competitors and their positioning
        - Comparative analysis of capabilities
        - Market share and differentiation

        ## 4. Internal Capability Assessment
        - Current organizational capabilities
        - Strengths and weaknesses analysis
        - Resource allocation and projects

        ## 5. Strategic Recommendations
        ### Immediate Actions (0-3 months)
        - Specific, actionable recommendations
        - Resource requirements
        - Expected outcomes

        ### Medium-term Initiatives (3-12 months)
        - Strategic projects and investments
        - Partnership opportunities
        - Capability development

        ### Long-term Strategy (1-3 years)
        - Vision and roadmap
        - Market positioning
        - Innovation pipeline

        ## 6. Risk Assessment
        - Market and competitive risks
        - Technical and implementation risks
        - Regulatory and compliance considerations

        ## 7. Key Metrics & KPIs
        - Success measurement criteria
        - Performance indicators
        - Monitoring framework

        GUIDELINES:
        - Use professional business language
        - Include specific data points and metrics when available
        - Use tables for comparisons when helpful
        - Bold key findings and recommendations
        - Include timelines and ownership suggestions
        - Cite sources appropriately
        - Acknowledge data limitations

        Focus on providing actionable business intelligence rather than just summarizing information.
        """
    
    def _enhanced_research_report(self, user_question, web_data, internal_data):
        """Professional mock research report"""
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        return f"""
# Comprehensive Research Report: {user_question}

**Report Date:** {current_date}  
**Prepared For:** Research Request  
**Prepared By:** AI Research Assistant

---

## Executive Summary

### Key Findings
- **Market Dynamics**: Significant advancements and increased competition in the sector
- **Internal Position**: Strong foundational capabilities with opportunities for expansion
- **Strategic Gap**: Alignment needed between current capabilities and market opportunities

### Immediate Recommendations
1. **Accelerate R&D investments** in core technology areas
2. **Establish strategic partnerships** to complement internal capabilities
3. **Enhance market intelligence** gathering and analysis

---

## 1. Market Overview & Current Landscape

### Current Market State
The market is experiencing rapid transformation with multiple technological breakthroughs. Key trends include increased automation, AI integration, and sustainability focus.

### Key Market Players
| Company | Market Position | Key Strength |
|---------|-----------------|--------------|
| Industry Leader A | Dominant | Technology Innovation |
| Company B | Strong Challenger | Market Reach |
| Emerging Player C | Growing | Specialized Solutions |

### Market Metrics
- **Market Size**: $XX Billion (2024)
- **Growth Rate**: XX% CAGR (2024-2028)
- **Key Drivers**: Technology adoption, regulatory changes, customer demand

---

## 2. Technical Analysis

### Current Capabilities
- **Maturity Level**: Advanced in core areas, developing in emerging technologies
- **Innovation Pipeline**: Multiple projects in development phase
- **Technical Debt**: Moderate, requiring strategic addressing

### Technology Trends
1. **AI & Machine Learning**: Increasing integration across solutions
2. **Cloud Native**: Shift towards cloud-based architectures
3. **API-first**: Emphasis on interoperability and integration

---

## 3. Competitive Landscape

### Strengths Comparison
| Aspect | Our Position | Market Leader | Key Differentiator |
|--------|--------------|---------------|-------------------|
| Technology | Advanced | Leading | Specialized focus |
| Market Reach | Regional | Global | Local expertise |
| Innovation | Strong R&D | Market driver | Research depth |

---

## 4. Internal Capability Assessment

### Current Projects
- **Project Alpha**: Next-generation platform development (75% complete)
- **Initiative Beta**: Market expansion program (planning phase)
- **Research Gamma**: Emerging technology exploration (early stage)

### Resource Allocation
- **R&D**: 40% of resources
- **Market Expansion**: 25% of resources  
- **Operations**: 35% of resources

---

## 5. Strategic Recommendations

### Immediate Actions (0-3 months)
1. **✅ Conduct competitive analysis workshop**
   - Timeline: Month 1
   - Owner: Strategy Team
   - Budget: $XX,XXX

2. **✅ Accelerate Project Alpha delivery**
   - Timeline: Months 1-3
   - Owner: Product Team
   - Expected Impact: XX% efficiency gain

### Medium-term Initiatives (3-12 months)
1. **🔄 Establish technology partnerships**
   - Timeline: Months 4-8
   - Owner: Business Development
   - Target: 2-3 strategic partners

2. **🔄 Enhance data analytics capabilities**
   - Timeline: Months 6-12
   - Owner: Data Science Team
   - Investment: $XXX,XXX

### Long-term Strategy (1-3 years)
1. **🚀 Market leadership position**
   - Target: Top 3 market position
   - Key Focus: Innovation and customer experience
   - Investment: Strategic acquisitions

---

## 6. Risk Assessment

### High Priority Risks
1. **Technology Disruption** (Probability: Medium, Impact: High)
   - Mitigation: Continuous R&D investment

2. **Market Competition** (Probability: High, Impact: Medium)
   - Mitigation: Differentiation strategy

3. **Regulatory Changes** (Probability: Medium, Impact: Medium)
   - Mitigation: Compliance monitoring

---

## 7. Key Metrics & KPIs

### Performance Indicators
- **Market Share**: Current XX%, Target: XX% by 2025
- **R&D ROI**: Target XX% return on research investments
- **Customer Satisfaction**: Maintain >90% satisfaction rate

### Success Criteria
- **Technology Leadership**: XX patents filed annually
- **Market Presence**: Expand to XX new markets
- **Financial Performance**: XX% revenue growth

---

*This report combines external market intelligence with internal organizational knowledge. Verify critical business decisions with additional primary research.*
"""

# Test the enhanced AI client
if __name__ == "__main__":
    client = FreeAIClient()
    
    test_question = "What are the latest advancements in quantum computing and our internal research position?"
    print("🧪 Testing Enhanced AI Client...")
    
    intent = client.analyze_intent(test_question)
    print(f"🎯 Enhanced Intent Analysis:\n{intent}")
    
    web_data = "External quantum computing breakthroughs"
    internal_data = "Internal quantum research projects"
    synthesis = client.synthesize_answer(test_question, web_data, internal_data)
    print(f"\n📊 Enhanced Report Preview:\n{synthesis[:500]}...")