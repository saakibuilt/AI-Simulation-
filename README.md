<div align="center">

<em>A Simple and Universal Swarm Intelligence Engine, Predicting Anything</em>

</div>

## ⚡ Overview

**Analytics Fish** is an AI-powered prediction engine that uses multi-agent simulations to forecast outcomes and generate predictions based on your data.

### How It Works

1. **Upload Your Data**: Provide a dataset (PDF, Markdown, or text files) as seed information for the simulation
2. **Define Your Goal**: Describe what you want to predict in natural language
3. **Create AI Agents**: The system automatically generates multiple AI agents with distinct personalities and memories
4. **Agent Interaction**: These agents interact with each other in a simulated environment, exploring scenarios and possibilities
5. **Final Interview**: An interview agent questions all the participating agents to gather insights and generate predictions
6. **Get Results**: Receive a comprehensive prediction report with detailed analysis

### Key Features

- **Simple to Use**: Just upload documents and describe your prediction goal
- **Multi-Agent Simulation**: Leverage swarm intelligence to explore complex scenarios
- **Interactive Reports**: Chat with agents and explore the simulation results
- **Flexible Applications**: Works for business predictions, creative writing, trend analysis, and more

### Use Cases

- Financial market predictions
- Policy impact analysis  
- News trend forecasting
- Story and creative writing generation
- Opinion polling and sentiment analysis
- Business decision forecasting

## 📸 Interface

<div align="center">
<img width="1918" height="977" alt="Screenshot 2026-05-29 at 3 26 26 PM" src="https://github.com/user-attachments/assets/560e5e11-fde2-4797-b190-29ed4886214e" />

*Analytics Fish user interface: Upload your data, describe your prediction goal, and let AI agents analyze and forecast outcomes*
</div>


> **Financial Prediction**, **Political News Prediction** and more examples coming soon...

## 🔄 Workflow

The Analytics Fish system follows a five-stage pipeline:

| Stage | Description |
|-------|-------------|
| **1. Graph Building** | Extract information from your uploaded data and create a knowledge graph representation |
| **2. Agent Generation** | Automatically generate AI agents with unique personalities and roles based on the data |
| **3. Simulation** | Run interactive simulation where agents engage with each other and explore different scenarios |
| **4. Report Generation** | Interview agents and compile findings into a comprehensive prediction report |
| **5. Interaction** | Chat with individual agents and the report agent to explore results in detail |

## 🚀 Quick Start

### Option 1: Source Code Deployment (Recommended)

#### Prerequisites

| Tool | Version | Description | Check Installation |
|------|---------|-------------|-------------------|
| **Node.js** | 18+ | Frontend runtime, includes npm | `node -v` |
| **Python** | ≥3.11, ≤3.12 | Backend runtime | `python --version` |
| **uv** | Latest | Python package manager | `uv --version` |

#### 1. Configure Environment Variables

```bash
# Copy the example configuration file
cp .env.example .env

# Edit the .env file and fill in the required API keys
```

**Required Environment Variables:**

```env
# LLM API Configuration (supports any LLM API with OpenAI SDK format)
# Recommended: Alibaba Qwen-plus model via Bailian Platform: https://bailian.console.aliyun.com/
# High consumption, try simulations with fewer than 40 rounds first
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Zep Cloud Configuration
# Free monthly quota is sufficient for simple usage: https://app.getzep.com/
ZEP_API_KEY=your_zep_api_key
```

#### 2. Install Dependencies

```bash
# One-click installation of all dependencies (root + frontend + backend)
npm run setup:all
```

Or install step by step:

```bash
# Install Node dependencies (root + frontend)
npm run setup

# Install Python dependencies (backend, auto-creates virtual environment)
npm run setup:backend
```

#### 3. Start Services

```bash
# Start both frontend and backend (run from project root)
npm run dev
```

**Service URLs:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`

**Start Individually:**

```bash
npm run backend   # Start backend only
npm run frontend  # Start frontend only
```

### Option 2: Docker Deployment

```bash
# 1. Configure environment variables (same as source deployment)
cp .env.example .env

# 2. Pull image and start
docker compose up -d
```

Reads `.env` from root directory by default, maps ports `3000 (frontend) / 5001 (backend)`

> Mirror address for faster pulling is provided as comments in `docker-compose.yml`, replace if needed.


## 📄 Acknowledgments

**Analytics Fish has received strategic support and incubation from Shanda Group!**

Analytics Fish's simulation engine is powered by **OASIS (Open Agent Social Interaction Simulations)**. We sincerely thank the CAMEL-AI team for their open-source contributions.



