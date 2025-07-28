# AI Agents System

A powerful terminal-based AI agents system that uses Google's Generative AI (Gemini) to create a master agent that can delegate tasks to specialized agents. The system features dynamic agent creation, similarity-based agent matching, and persistent storage of agents.

## Features

- **Master-Agent Delegation**: Central master agent coordinates and delegates tasks to specialized agents
- **Dynamic Agent Creation**: Automatically creates new specialized agents when needed
- **Similarity Search**: Finds existing agents that match task requirements to avoid duplication
- **Persistent Storage**: Agents are saved in JSON format for reuse across sessions
- **Terminal Interface**: Simple command-line interface for easy interaction
- **Hierarchical Task Management**: Agents can delegate to other agents for complex workflows

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│  Master Agent   │───▶│ Similarity Search│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Task Analysis   │    │ Existing Agents │
                       └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  New Agent      │◀───│ Agent Storage   │
                       │  Creation       │    │    (JSON)       │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Task Delegation │
                       └─────────────────┘
```

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" in the top right
4. Create a new API key
5. Copy the key (it should start with `AIza...`)

### 2. Set Up Environment

#### Option A: Using Replit (Recommended)
1. Clone this repository to Replit
2. Add your API key to Replit Secrets:
   - Go to Tools > Secrets
   - Add key: `GEMINI_API_KEY`
   - Add value: Your Gemini API key
3. Run the project

#### Option B: Local Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-agents-system
   ```

2. Install dependencies:
   ```bash
   pip install google-genai numpy
   ```

3. Set environment variable:
   ```bash
   export GEMINI_API_KEY='your_api_key_here'
   ```

## Usage

### Running the System

Start the AI agents system:

```bash
python main.py
```

You'll see the welcome interface:

```
============================================================
🤖 AI Agents System - Terminal Interface
============================================================
Welcome! You can interact with the master agent.
The master agent will delegate tasks to specialized agents.
Type 'quit', 'exit', or 'q' to exit the system.
------------------------------------------------------------
✅ Master agent initialized successfully!
------------------------------------------------------------
🗣️  You: 
```

### Example Interactions

#### 1. Programming Tasks
```
🗣️  You: Write a Python function to calculate fibonacci numbers

🔨 Creating new specialized agent...
✅ Created and saved new agent: PythonCodingAgent
🔄 Delegating to agent: PythonCodingAgent

✨ Master Agent: Here's a Python function to calculate Fibonacci numbers:

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

# Example usage:
print(fibonacci(10))  # Output: 55
```

#### 2. Creative Writing
```
🗣️  You: Write a short story about a robot learning to paint

🔨 Creating new specialized agent...
✅ Created and saved new agent: CreativeWritingAgent
🔄 Delegating to agent: CreativeWritingAgent

✨ Master Agent: **The Canvas of Dreams**

In the quiet corner of an art studio, Unit-7 stood motionless before an easel...
[Full creative story response]
```

#### 3. Educational Content
```
🗣️  You: Explain quantum computing in simple terms

📋 Found existing agent: EducationAgent
🔄 Delegating to agent: EducationAgent

✨ Master Agent: Quantum computing is like having a magical computer...
[Detailed explanation]
```

#### 4. Mathematical Problems
```
🗣️  You: Help me solve this math problem: What is 15% of 240?

🔨 Creating new specialized agent...
✅ Created and saved new agent: MathAgent
🔄 Delegating to agent: MathAgent

✨ Master Agent: To find 15% of 240:
Step 1: Convert percentage to decimal: 15% = 0.15
Step 2: Multiply: 240 × 0.15 = 36
Answer: 15% of 240 is 36
```

### Agent Reuse

The system automatically reuses existing agents when appropriate:

```
🗣️  You: Write a JavaScript function for sorting arrays

📋 Found existing agent: CodingAgent
🔄 Delegating to agent: CodingAgent

✨ Master Agent: [JavaScript sorting function response]
```

## Project Structure

```
ai-agents-system/
├── main.py                 # Entry point and terminal interface
├── master_agent.py         # Master agent implementation
├── base_agent.py          # Base agent class and specialized agent
├── agent_storage.py       # JSON-based agent persistence
├── similarity_search.py   # Agent similarity matching
├── utils.py               # Utility functions and logging
├── test_system.py         # Test script for functionality
├── agents_storage.json    # Agent storage file (created automatically)
├── agents_system.log      # System logs (created automatically)
└── README.md              # This file
```

## Key Components

### 1. Master Agent (`master_agent.py`)
- Analyzes user requests using Gemini AI
- Determines if delegation is needed
- Creates or finds appropriate specialized agents
- Delegates tasks and returns responses

### 2. Agent Storage (`agent_storage.py`)
- Persists agents in JSON format
- Handles CRUD operations for agents
- Maintains data integrity and error recovery

### 3. Similarity Search (`similarity_search.py`)
- Uses multiple similarity algorithms (Jaccard, keyword overlap, cosine similarity)
- Finds existing agents that match new task requirements
- Prevents duplicate agent creation

### 4. Base Agent (`base_agent.py`)
- Abstract base class for all agents
- Provides common functionality and serialization
- Defines the agent interface

## Configuration

### Similarity Threshold
You can adjust the similarity threshold for agent matching in `similarity_search.py`:

```python
def __init__(self, similarity_threshold: float = 0.6):
```

Lower values (0.4-0.5) create fewer agents but may reuse less suitable ones.
Higher values (0.7-0.8) create more specialized agents but may duplicate functionality.

### Logging Level
Adjust logging verbosity in `utils.py`:

```python
def setup_logging(log_level: str = "INFO", log_file: str = "agents_system.log"):
```

Available levels: DEBUG, INFO, WARNING, ERROR

## Testing

Run the test script to verify functionality:

```bash
python test_system.py
```

This will:
- Test the master agent initialization
- Try various types of requests
- Show agent creation and reuse
- Display storage statistics

## Troubleshooting

### Common Issues

1. **API Key Invalid**
   ```
   Error: API key not valid
   ```
   - Verify your API key is correct
   - Ensure it starts with "AIza..."
   - Check it's properly set in environment variables

2. **No Agent Creation**
   ```
   No agents created for simple requests
   ```
   - This is normal - simple requests are handled directly by the master agent
   - Only complex requests that benefit from specialization create new agents

3. **Storage File Errors**
   ```
   Storage file corrupted
   ```
   - The system automatically recreates corrupted storage files
   - Check file permissions in the project directory

### Debug Mode

Enable debug logging for detailed information:

```python
setup_logging(log_level="DEBUG")
```

This shows:
- Detailed similarity scores
- Agent creation decisions
- API request/response details
- Storage operations

## Advanced Usage

### Programmatic Access

You can use the system programmatically:

```python
from master_agent import MasterAgent
from utils import setup_logging

# Setup
setup_logging()
master = MasterAgent()

# Process requests
response = master.process_request("Your request here")
print(response)

# Get storage stats
stats = master.agent_storage.get_storage_stats()
print(f"Total agents: {stats['total_agents']}")
```

### Custom Agent Types

The system automatically creates agents for these categories:
- **coding**: Programming and development tasks
- **writing**: Creative and technical writing
- **research**: Information gathering and analysis
- **math**: Mathematical calculations and problems
- **creative**: Art, stories, and creative content
- **analysis**: Data analysis and interpretation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `agents_system.log`
3. Test with the provided test script
4. Open an issue with detailed error information

---

**Note**: This system requires an active internet connection to communicate with Google's Gemini AI service. Ensure your API key has sufficient quota for your usage needs.