# Quickstart: Reusable Intelligence via Claude Subagents & Agent Skills

## Overview
This guide shows how to quickly get started with the subagent system for humanoid robotics textbook assistance.

## Prerequisites
- Python 3.11+
- Anthropic API key configured
- Existing backend dependencies installed

## Setup

### 1. Initialize the Agent System
```python
from backend.agent.agent_router import AgentRouter
from backend.agent.skill_registry import SkillRegistry

# Initialize the system
router = AgentRouter()
skill_registry = SkillRegistry()
router.initialize_agents()
```

### 2. Available Agents

#### Book Expert Agent
- Purpose: Answer complex questions using full-book RAG capabilities
- Usage: For questions that span multiple chapters or require comprehensive understanding
- Example: `"Explain the relationship between perception and action in humanoid robotics"`

#### Selected Text Reasoner
- Purpose: Analyze specific text selections without external context
- Usage: For focused analysis of particular passages
- Example: `"Analyze this text: [selected text here]"`

#### Chapter Guide Agent
- Purpose: Explain concepts at different difficulty levels (beginner/intermediate/advanced)
- Usage: For personalized learning experiences
- Example: `"Explain inverse kinematics at beginner level"`

#### Evaluation Agent
- Purpose: Check responses for hallucinations and context leakage
- Usage: For quality assurance of AI-generated content
- Example: `"Evaluate this response: [response text here]"`

### 3. Making Requests

#### Using the API
```bash
# Route to appropriate agent automatically
curl -X POST http://localhost:5000/api/subagent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Your question here",
    "user_context": {"difficulty_preference": "intermediate"}
  }'

# Call specific agent
curl -X POST http://localhost:5000/api/subagent/book-expert \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Complex question spanning multiple chapters",
    "context": "full_book"
  }'
```

#### Using the Python Interface
```python
from backend.agent.agent_router import AgentRouter

router = AgentRouter()
response = router.route_request({
    "query": "Explain humanoid gait control",
    "user_intent": "understanding",
    "difficulty": "intermediate"
})
print(response)
```

### 4. Registering New Skills
```python
from backend.agent.skill_registry import register_skill

@register_skill(
    id="custom_analysis",
    name="Custom Analysis Skill",
    description="Performs custom analysis on text",
    input_schema={"text": "string", "analysis_type": "string"},
    output_schema={"result": "object"}
)
def custom_analysis_skill(text: str, analysis_type: str):
    # Implementation here
    return {"result": "analysis_result"}
```

### 5. Creating New Agents
```python
from backend.agent.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="custom_agent",
            description="A custom agent for specific tasks",
            skills=["custom_analysis", "retrieve_book_chunks"]
        )

    def process_request(self, request_data):
        # Custom processing logic
        pass
```

## Integration with Existing System
The subagent system integrates seamlessly with the existing chatbot:
- Existing `/api/chat` endpoint now supports agent routing
- Backward compatibility maintained - existing functionality preserved
- New agent-specific endpoints available for direct access