# Drone Security Analyst Agent

A prototype AI-powered security monitoring system for docked drones that processes live telemetry data and video feeds to detect and analyze security events in real-time.

## Features

- **Real-time Video Analysis**: Uses Florence-2 Vision-Language Model (VLM) to analyze video frames and generate detailed descriptions
- **Rule-based Alert System**: Automatically detects security events like unauthorized vehicles or nighttime loitering
- **Frame-by-frame Indexing**: Stores analyzed frames in a vector database (ChromaDB) for efficient querying and retrieval
- **Interactive Query Agent**: LangChain-powered agent that answers security-related questions using indexed data and conversation history
- **Telemetry Integration**: Processes drone position, altitude, and timestamp data alongside video analysis

## Value Proposition

This agent enhances property security by providing automated 24/7 monitoring that:
- Identifies and logs suspicious objects or activities (e.g., "Blue Ford F150 entered twice today")
- Generates immediate alerts for security threats (e.g., "Person loitering at midnight near main gate")
- Maintains searchable historical records for forensic analysis
- Reduces response time to security incidents through automated detection

## Architecture

The system follows a modular pipeline architecture:

1. **Data Ingestion**: Processes simulated telemetry data and video frames
2. **Vision Analysis**: Florence-2 VLM generates detailed captions for each frame
3. **Rule Engine**: Applies predefined security rules to detect events and generate alerts
4. **Indexing Layer**: Stores frame descriptions and metadata in ChromaDB for semantic search
5. **Query Interface**: LangChain agent provides natural language querying capabilities

```
[Telemetry Data] --> [Vision Engine] --> [Alert System] --> [Vector DB]
                              |              |
                              v              v
                       [Frame Descriptions] [Security Alerts]
                                             |
                                             v
                                   [Query Agent Interface]
```

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for VLM processing)
- Ollama with Llama 3.2 model installed
- 8GB+ RAM recommended

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rushizzz/drone-security-agent.git
   cd drone-security-agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama and model**:
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai)
   ollama pull llama3.2
   ```

5. **Prepare video data** (optional - for frame extraction):
   Place your drone footage video as `drone-footage.mp4` in the root directory.

## Usage

### Running the Security Pipeline

Execute the main pipeline to process simulated data:

```bash
python app.py
```

This will:
- Process all frames in `simulation_data.json`
- Generate VLM descriptions for each frame
- Apply security rules and generate alerts
- Index all data in the vector database

### Interactive Query Mode

After pipeline execution, the system enters interactive mode where you can ask security-related questions:

```
Welcome to the Drone Security Analyst Agent!
Type 'exit' to quit.

[Analyst Query]: What vehicles were spotted today?
[Agent Response]: Based on the security logs, a blue Ford F150 was identified at the Main Gate and Garage locations.

[Analyst Query]: Were there any nighttime activities?
[Agent Response]: Yes, a person was detected loitering at the Main Gate at 00:01:00 on 2026-03-23.
```

### Frame Extraction (Optional)

To extract frames from a video file:

```bash
python extract_frames.py
```

This extracts frames every 45 seconds (configurable) from `drone-footage.mp4` to the `extracted_frames/` directory.

## Configuration

### Simulation Data

The system uses `simulation_data.json` for simulated telemetry and frame data. Each entry contains:
- `frame_id`: Unique frame identifier
- `timestamp`: ISO format timestamp
- `location`: Drone location (e.g., "Main Gate", "Garage")
- `image`: Path to frame image file

### Security Rules

Currently implemented rules in `main_agent.py`:
- Blue truck detection: Logs "Blue Ford F150" identifications
- Nighttime loitering: Alerts for persons detected between 22:00-04:00

### VLM Configuration

Florence-2 model settings in `vision_engine.py`:
- Task prompt: `<DETAILED_CAPTION>` for comprehensive descriptions
- Generation parameters: max_new_tokens=1024, num_beams=3

## Design Decisions

### Technology Choices

- **Florence-2 VLM**: Chosen for its strong performance in detailed image captioning without requiring massive computational resources. Provides more accurate object detection compared to CLIP or BLIP for security monitoring scenarios.

- **ChromaDB**: Lightweight vector database perfect for frame-by-frame indexing. Enables semantic search across frame descriptions for efficient querying.

- **LangChain + Ollama**: Combines LangChain's agent framework with local Llama 3.2 model for privacy-preserving, cost-effective conversational AI without external API dependencies.

- **Rule-based Alerting**: Simple, interpretable rules ensure reliable detection of known security patterns while being easily extensible.

### Architecture Rationale

- **Modular Design**: Separates concerns (vision, alerting, indexing, querying) for maintainability and testing
- **Local Processing**: All AI models run locally to ensure data privacy and reduce latency
- **Extensible Rules**: Rule engine can be easily enhanced with ML-based detection as needed
- **Semantic Indexing**: Vector search enables natural language queries about security events

## AI Tools Integration

This project was developed using AI-assisted tools throughout the development process:

### Claude Code
- **Architecture Design**: Generated initial system architecture and component breakdown
- **Code Generation**: Created the LangChain agent implementation and ChromaDB integration
- **Debugging**: Assisted in resolving VLM model loading issues and CUDA configuration
- **Documentation**: Helped structure the README and report documentation

### Cursor AI
- **Vision Engine**: Implemented Florence-2 model integration with proper preprocessing
- **Rule Logic**: Developed the alert system with time-based and object-based rules
- **Testing**: Created test cases and validation scenarios

### Windsurf
- **Data Pipeline**: Built the main processing pipeline with error handling
- **Query Interface**: Designed the conversational agent with context management

### Impact on Workflow
AI tools accelerated development by:
- Reducing research time for unfamiliar technologies (Florence-2, ChromaDB)
- Providing code templates and best practices
- Assisting with debugging and optimization
- Generating comprehensive documentation

Without AI assistance, implementation would have taken significantly longer, especially for the cross-domain indexing component which was new to the developer.

## Testing

The system includes basic validation through the pipeline execution. Test scenarios include:

- Vehicle detection accuracy
- Alert triggering at appropriate times
- Database indexing and retrieval
- Query agent responses

For comprehensive testing, run the pipeline and verify:
- Correct logging of "Blue Ford F150" events
- Nighttime person alerts
- Successful indexing (check `drone_db/` directory)
- Query responses contain relevant information

## Future Enhancements

- **Video Summarization**: Add capability to generate 1-sentence video summaries
- **Advanced ML Detection**: Replace rule-based system with trained object detection models
- **Real-time Streaming**: Integrate with actual drone video feeds
- **Multi-camera Support**: Handle multiple drone viewpoints
- **Alert Escalation**: Email/SMS notifications for critical alerts
- **Dashboard UI**: Web interface for monitoring and querying

## License

This project is licensed under the [Apache License 2.0](LICENSE).
