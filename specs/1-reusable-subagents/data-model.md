# Data Model: Reusable Intelligence via Claude Subagents & Agent Skills

## Key Entities

### Agent
- **name**: string - Unique identifier for the agent
- **description**: string - Human-readable description of the agent's purpose
- **skills**: list[string] - List of skill IDs that the agent can utilize
- **routing_rules**: list[object] - Rules for determining when to use this agent
- **config**: object - Agent-specific configuration parameters

### Skill
- **id**: string - Unique identifier for the skill
- **name**: string - Human-readable name of the skill
- **description**: string - Description of what the skill does
- **input_schema**: object - JSON schema defining expected input parameters
- **output_schema**: object - JSON schema defining expected output format
- **implementation**: string - Reference to the implementation function

### AgentRequest
- **id**: string - Unique request identifier
- **agent_type**: string - Type of agent to handle the request
- **input_data**: object - Input data for the agent
- **user_context**: object - Information about the requesting user
- **timestamp**: datetime - When the request was made
- **metadata**: object - Additional request metadata

### AgentResponse
- **request_id**: string - Reference to the original request
- **agent_used**: string - Which agent processed the request
- **output_data**: object - Output data from the agent
- **status**: string - Status of the response (success, error, partial)
- **timestamp**: datetime - When the response was generated
- **evaluation**: object - Results from evaluation agent (if applicable)

## Relationships

- An Agent can utilize multiple Skills
- An AgentRequest is processed by one Agent
- An AgentResponse corresponds to one AgentRequest
- Skills can be shared across multiple Agents

## Validation Rules

- Agent names must be unique within the system
- Skill IDs must follow the format: `[a-z_]+`
- AgentRequest input_data must match the input_schema of the target agent/skills
- AgentResponse status must be one of: 'success', 'error', 'partial', 'timeout'