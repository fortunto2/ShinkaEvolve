# Evolving Startup Agent with SGR and Web Research

An evolving startup strategy development agent that combines Schema-Guided Reasoning (SGR) with web research to analyze startup ideas and generate quantitative, SEO-focused business analyses. Optimized for seasonal businesses launching in 3 months for Christmas 2025-2026.

## 🎯 Overview

**🧬 EVOLVE-BLOCK Parameters:** ShinkaEvolve mutates research depth, analysis weights, SEO focus, and strategy parameters to optimize startup analysis quality.

**📊 Quantitative Focus:** Generates specific numbers - market size ($), search volumes, CAC/LTV, revenue projections, break-even analysis.

**🔍 SEO-Driven Strategy:** Targets seasonal traffic surge for Christmas 2025-2026 with keyword research and content strategy.

### Analysis Pipeline:
1. **Enhanced Market Research** - Configurable depth web research (5-8 queries)
2. **SEO Opportunity Analysis** - Keyword research with search volumes and difficulty
3. **Competitive Intelligence** - Revenue estimates, domain authority, traffic data
4. **Quantitative Analysis** - Financial projections, funding requirements, break-even
5. **Evolution Fitness** - Multi-component scoring for genetic algorithm optimization

## 🏗️ Architecture

### SGR Integration
- **Structured Outputs**: All LLM responses use Pydantic schemas for reliability
- **Iterative Refinement**: Strategies evolve through criticism and improvement cycles
- **Type Safety**: Full type checking and validation of all analysis outputs

### Web Research Integration
- **Market Intelligence**: Automated market size and opportunity research
- **Competitive Analysis**: Comprehensive competitor landscape mapping
- **Trend Analysis**: Market trend identification and validation
- **Evidence-Based**: All analysis backed by real web research data

### ShinkaEvolve Evolution
- **Fitness Function**: Multi-component scoring (strategy quality + research + efficiency)
- **Mutation Targets**: Strategy parameters, research depth, iteration counts
- **Selection Pressure**: Optimizes for comprehensive, actionable PRDs

## 📊 Components

### Core Files
- `initial.py` - Main agent implementation with EVOLVE-BLOCK
- `startup_sgr_schemas.py` - Pydantic schemas for all structured outputs
- `tavily_integration.py` - Web research integration via localhost Tavily
- `evaluate.py` - Fitness evaluation for ShinkaEvolve

### SGR Schemas
- `NicheAnalysis` - Market niche and opportunity analysis
- `CompetitorProfile` - Competitive landscape mapping
- `MarketStrategy` - Strategic approaches and execution plans
- `CriticalEvaluation` - Strategy assessment and improvement recommendations
- `StartupPRD` - Comprehensive product requirements document

## 🚀 Usage

### Basic Usage
```python
from initial import StartupAgent, StartupAgentConfig

config = StartupAgentConfig(
    max_iterations=3,
    strategy_count=5,
    model_names=["gpt-5-mini"],
    enable_deep_research=True
)

agent = StartupAgent(config)

startup_idea = """
AI-powered task management app that learns user patterns
and automatically prioritizes tasks based on deadlines,
importance, and personal work habits.
"""

# Run analysis (async)
prd = await agent.analyze_startup_idea(startup_idea)
agent.save_results()
```

### ShinkaEvolve Integration
```bash
# Launch evolution
shinka_launch task=startup_agent database=island_small evolution=sgr_small_budget

# Monitor progress
shinka_visualize --port 8888 --open
```

## 📋 Example Output

The agent generates structured outputs at each stage:

### Niche Analysis
```json
{
  "market_segment": "AI-powered productivity tools",
  "market_size": {
    "opportunity": "Task management software market",
    "market_size_usd": 4200000000,
    "growth_rate": 0.13,
    "difficulty": "medium"
  },
  "target_customers": [
    {
      "segment_name": "Knowledge workers",
      "size_estimate": 1000000,
      "pain_points": ["Task overload", "Poor prioritization"],
      "willingness_to_pay": "medium"
    }
  ]
}
```

### Strategy Development
```json
{
  "approach": "Freemium AI-first productivity platform",
  "value_proposition": {
    "primary_benefit": "Automated intelligent task prioritization",
    "unique_differentiator": "Learns individual work patterns",
    "proof_points": ["Reduces decision fatigue", "Improves productivity"]
  },
  "monetization": {
    "model_type": "freemium",
    "pricing_strategy": "Usage-based premium features"
  }
}
```

### Final PRD
Complete product requirements document with:
- Product vision and positioning
- Core feature specifications with acceptance criteria
- Technical requirements and architecture
- Go-to-market strategy
- Success metrics and KPIs
- Risk assessment and mitigation
- Development roadmap

## ⚙️ Configuration

### Agent Configuration
```python
@dataclass
class StartupAgentConfig:
    max_iterations: int = 3          # Strategy refinement cycles
    strategy_count: int = 5          # Number of strategies to generate
    criticism_threshold: float = 0.7  # Quality threshold for convergence
    model_names: List[str] = ["gpt-5-mini"]
    enable_deep_research: bool = True
    tavily_localhost: str = "http://localhost:8000"
```

### Web Research Setup
Requires Tavily search service running on localhost:
```bash
# Start Tavily service (example)
cd /path/to/sgr-deep-research
python -m sgr_deep_research.services.tavily_search --port 8000
```

## 🎯 Evolution Strategy

The agent is designed for ShinkaEvolve optimization:

### Mutation Targets (EVOLVE-BLOCK)
- Strategy generation parameters
- Research depth and scope
- Iteration and convergence thresholds
- LLM model selection and temperature

### Fitness Components
1. **Strategy Quality (50%)** - PRD completeness, feature detail, risk assessment
2. **Research Completeness (30%)** - Market validation, competitive analysis depth
3. **Iteration Efficiency (20%)** - Time to convergence, iteration optimization

### Success Metrics
- Combined fitness score > 0.8
- Complete PRD with 5+ features
- 3+ iterations with strategy refinement
- Evidence-based market validation

## 🧪 Testing

### Unit Testing
```bash
cd examples/startup_agent
python -m pytest tests/
```

### Integration Testing
```bash
# Test web research integration
python tavily_integration.py

# Test full agent pipeline
python initial.py

# Test evaluation scoring
python evaluate.py
```

### Evolution Testing
```bash
# Single evaluation run
python evaluate.py

# Full evolution run
shinka_launch examples/startup_agent
```

## 🔧 Development

### Adding New Research Sources
1. Extend `TavilyWebResearch` class
2. Add new research methods (e.g., `research_pricing`, `research_regulations`)
3. Update agent workflow in `_analyze_niche`

### Extending SGR Schemas
1. Add new Pydantic models to `startup_sgr_schemas.py`
2. Create corresponding LLM clients in `StartupAgent.__init__`
3. Integrate into analysis workflow

### Custom Fitness Functions
1. Modify evaluation components in `evaluate.py`
2. Add new scoring dimensions
3. Adjust weights in `run_shinka_eval`

## 📈 Performance

### Typical Execution
- **Analysis Time**: 2-4 minutes for complete analysis
- **Research Depth**: 20-50 web sources per startup idea
- **Strategy Generation**: 5 initial strategies with 3 refinement cycles
- **PRD Quality**: 5-8 core features with detailed acceptance criteria

### Scalability
- Parallel strategy evaluation
- Cached web research results
- Async execution throughout pipeline
- Configurable depth vs speed tradeoffs

## 🚦 Roadmap

### Near Term
- [ ] Enhanced competitor intelligence
- [ ] Financial modeling integration
- [ ] User persona development
- [ ] Technical architecture generation

### Medium Term
- [ ] Multi-language market research
- [ ] Regulatory compliance analysis
- [ ] Partnership opportunity identification
- [ ] Funding strategy recommendations

### Long Term
- [ ] Real-time market monitoring
- [ ] Automated MVP generation
- [ ] Launch strategy optimization
- [ ] Post-launch performance tracking