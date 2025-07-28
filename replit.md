# AI Agents System

## Overview

This is a Python-based AI agents system that uses Google's Generative AI (Gemini) to create a master agent that can delegate tasks to specialized agents. The system features dynamic agent creation, similarity-based agent matching, and persistent storage of agents using JSON files.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The system follows a modular, object-oriented architecture with the following key principles:

### Core Architecture Pattern
- **Master-Agent Delegation Pattern**: A central master agent coordinates and delegates tasks to specialized agents
- **Factory Pattern**: Dynamic creation of specialized agents based on task requirements
- **Repository Pattern**: Abstracted storage layer for agent persistence

### Technology Stack
- **Language**: Python 3
- **AI Service**: Google Generative AI (Gemini API)
- **Storage**: JSON file-based persistence
- **Search**: Text-based similarity search with vector-like scoring
- **Interface**: Terminal-based command-line interface

## Key Components

### 1. Master Agent (`master_agent.py`)
- **Purpose**: Central coordinator that processes user requests and delegates to specialized agents
- **Responsibilities**: 
  - Request analysis and routing
  - Dynamic agent creation
  - Agent lifecycle management
  - Integration with Gemini API

### 2. Base Agent (`base_agent.py`)
- **Purpose**: Abstract base class providing common functionality for all agents
- **Responsibilities**:
  - Common agent properties (name, description, timestamps)
  - Serialization interface
  - Basic agent information management

### 3. Agent Storage (`agent_storage.py`)
- **Purpose**: Handles persistence and retrieval of agents
- **Technology**: JSON file storage
- **Responsibilities**:
  - CRUD operations for agents
  - File validation and error recovery
  - Data integrity maintenance

### 4. Similarity Search (`similarity_search.py`)
- **Purpose**: Finds existing agents that match task requirements
- **Algorithm**: Text-based similarity scoring
- **Responsibilities**:
  - Agent matching based on descriptions
  - Similarity threshold management
  - Search optimization

### 5. Main Interface (`main.py`)
- **Purpose**: Entry point and user interface
- **Responsibilities**:
  - Environment validation (API key checks)
  - User interaction loop
  - Error handling and graceful shutdown

### 6. Utilities (`utils.py`)
- **Purpose**: Common utility functions
- **Responsibilities**:
  - Logging configuration
  - System-wide helper functions

## Data Flow

1. **User Input**: User enters request through terminal interface
2. **Request Processing**: Master agent analyzes the request using Gemini API
3. **Agent Discovery**: Similarity search looks for existing suitable agents
4. **Agent Creation/Selection**: Either reuse existing agent or create new specialized agent
5. **Task Delegation**: Master agent delegates task to selected/created agent
6. **Response Generation**: Specialized agent processes task and returns response
7. **Persistence**: New agents are stored in JSON storage for future reuse

## External Dependencies

### Required APIs
- **Google Generative AI (Gemini)**: Primary AI service for request processing and agent creation
  - Requires `GEMINI_API_KEY` environment variable
  - Used for natural language understanding and response generation

### Python Libraries
- `google-genai`: Official Google Generative AI client
- `numpy`: For similarity calculations (implied from similarity search logic)
- Standard library modules: `json`, `logging`, `os`, `sys`, `typing`, `abc`, `datetime`

## Deployment Strategy

### Environment Setup
- **API Key Management**: System validates presence of `GEMINI_API_KEY` on startup
- **File Permissions**: Requires read/write access for JSON storage files
- **Logging**: Configurable logging to both file and console

### Storage Strategy
- **Local JSON Files**: Agents stored in `agents_storage.json`
- **Auto-Recovery**: System handles corrupted storage files by recreating them
- **Data Format**: Structured JSON with agent metadata and serialized state

### Scalability Considerations
- **Current Limitations**: Single-file JSON storage limits scalability
- **Future Improvements**: Architecture supports migration to database backends
- **Search Performance**: Text-based similarity search may need optimization for large agent collections

### Error Handling
- **Graceful Degradation**: System continues operation even with storage issues
- **API Failures**: Proper error handling for Gemini API connectivity issues
- **User Experience**: Clear error messages and recovery instructions

## Key Architectural Decisions

### Storage Choice: JSON Files
- **Rationale**: Simple deployment, no database dependencies, human-readable format
- **Trade-offs**: Limited scalability, no concurrent access support
- **Future Migration**: Architecture abstracts storage behind repository pattern

### Similarity Search: Text-Based
- **Rationale**: No external vector database required, simple implementation
- **Trade-offs**: Less sophisticated than semantic embeddings
- **Extensibility**: Interface allows for future vector-based implementations

### Agent Lifecycle: Dynamic Creation
- **Rationale**: Flexible system that adapts to user needs
- **Benefits**: No pre-defined agent limitations, personalized agent creation
- **Challenges**: Potential for agent proliferation, storage management complexity

## Recent Changes: Latest modifications with dates

### 2025-07-28: Documentation and Setup Enhancement
- **README.md**: Created comprehensive documentation with setup instructions, usage examples, and troubleshooting guide
- **DEPENDENCIES.md**: Added detailed dependency information and installation instructions  
- **setup.py**: Created automated setup verification script to check Python version, dependencies, API key, and storage structure
- **examples.py**: Added interactive example script with 25+ sample requests across 5 categories (Programming, Creative, Educational, Analysis, Mathematics)
- **test_system.py**: Enhanced test script for system validation
- **Project Status**: Fully functional AI agents system with complete documentation and setup tools