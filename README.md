# Connect Four AI

## Project Overview
This project implements an AI-powered Connect Four game, featuring a minimax algorithm with alpha-beta pruning for optimal gameplay.

## Features
- Interactive command-line Connect Four game
- AI opponent using advanced search algorithms
- Customizable board size and difficulty levels
- Unit tests for core functionality

## Installation
### Prerequisites
- Python 3.8 or higher
- uv package manager

### Setup with uv
1. Install uv if not already installed:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

2. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/connect-four-ai.git
  cd connect-four-ai
  ```

3. Create a virtual environment and install dependencies:
  ```bash
  uv venv
  uv pip install -e .
  ```

## Usage
Run the game:
```bash
uv run main.py
```
