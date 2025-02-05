# k

**k** is a personal command-line interface (CLI) tool designed to help me automate and streamline tasks like transcribing audio files, assimilating voice memos into notes, prompting AI agents, and more. It leverages a variety of services and integrations (OpenAI, Amazon Transcribe, Discord bots, etc.) to provide a flexible, extensible system for personal productivity and note management.

---

## Table of Contents

- [k](#k)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Commands Overview](#commands-overview)
      - [Subcommands under `run`](#subcommands-under-run)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Extending k](#extending-k)
  - [Running Tests](#running-tests)

---

## Features

- **Voice Memo Assimilation**: Record daily voice notes and assimilate them into a central note for easy retrieval.  
- **Audio Transcription**: Transcribe audio files using external services (e.g., AWS Transcribe or OpenAI Whisper).  
- **AI Agent Integration**: Prompt AI agents for Q&A, search, scheduling tasks, or more advanced use cases.  
- **Document Indexing**: Index local documents and notes for quick searching.  
- **Discord Bot**: Run a Discord bot that can leverage your AI agents and indexing capabilities.

---

## Requirements

- **Python 3.8+** (Ensure you have a compatible version installed.)  
- Pipenv or virtualenv (recommended) for Python dependency management

---

## Installation

1. **Clone the Repository:**
   - `git clone https://github.com/goodhanded/k.git`
   - `cd k`

2. **Create and activate a virtual environment**
   - `python -m venv venv` (from project root)
   - `. ./venv/bin/activate`

3. **Install Dependencies:**
   - `pip install -r requirements.txt`

4. **(Optional) Set Up Environment Variables:**
   - Depending on the integrations you plan to use (OpenAI, AWS, Discord), you may need to set environment variables such as `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DISCORD_BOT_TOKEN`, etc.
   - Copy .env.example to .env to set these variables for local development

5. **Add bash/zsh alias**
   - In .zshrc, add `alias k='/path/to/k/venv/bin/python /path/to/k/k.py'`
   - Now you can just call `k` rather than `python k.py` 

6. **Run the CLI:**
   - `k --help`

---

## Usage

All commands are defined in `commands.yaml`. To run a command, use:
`k <command> [args...]`

For subcommands:
`k run <subcommand> [args...]`

### Commands Overview

Here are the primary commands and their definitions:

| Command        | Usage Example                                                  | Description                                                                   |
| -------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **assimilate** | `k assimilate --path /path/to/audio.wav`           | Assimilates a voice memo into your daily note (requires a local audio file). |
| **transcribe** | `k transcribe --path /path/to/audio.wav`           | Transcribes the given audio file.                                            |
| **ask**        | `k ask --agent_name search_agent --prompt "Hello!"` | Prompts an AI agent with a given text input.                                 |
| **run**        | `k run discord`                                     | Runs one of the subcommands, e.g. `discord` or `indexer`.                    |

#### Subcommands under `run`

- **discord**  
  Runs the Discord bot, which can respond to user prompts using your AI agents.

- **indexer**  
  Indexes documents in your configured storage for quick searching and retrieval.

### Examples

1. **Transcribe an Audio File**  
   `k transcribe --path ~/recordings/todays_notes.wav`  
   This will produce a transcription for the audio file.

2. **Assimilate a Voice Memo**  
   `k assimilate --path ~/recordings/daily_update.wav`  
   This adds the transcribed memo into your daily note (for example, in Obsidian).

3. **Ask an AI Agent**  
   `k ask --agent_name search_agent --prompt "What's the weather like in San Francisco?"`  
   This sends the prompt to the specified agent. The agent’s response is printed to your console (and could be logged elsewhere, depending on your config).

4. **Run Discord Bot**  
   `k run discord`  
   This starts the Discord bot. Ensure your environment variables contain your bot token.

---

## Configuration

- **commands.yaml**  
  Defines CLI commands, their help text, the function to execute, and accepted arguments.

- **services.yaml**  
  Declares services like the transcriber, search engine, or any other integrations needed.

- **Application-wide Settings**  
  Configured in `.env`, read by  `application/config` and injected into service constructors via the dependency injection (DI) container in `infrastructure/di`.

You can further customize these to extend functionality or adapt to your specific environment, such as choosing a different transcriber service or search engine.

---

## Extending k

1. **Add a New Python Dependency**
   - Update `requirements.in` with the python dependency you want to add.
   - Run `pip-compile requirements.in --strip-extras` to compile a new requirements.txt file.
   - Run `pip install -r requirements.txt` to install the dependencies in the requirements.txt file.

2. **Add a New Command**  
   - Create or update a `use_case` in the appropriate `application/...` folder.  
   - Reference that use case in `commands.yaml` by specifying a `target` that points to its DI container name (for example, `@agency.some_use_case.execute`).

3. **Add a New AI Agent**  
   - Implement the agent logic in `infrastructure/agency/services/agents`.  
   - Register it via the DI container in `services.yaml`.
   - Tag it with `{ name: agent, alias: <alias> }` to have the di container add it to the agent registry.

4. **Add a New Service**  
   - Create a service class (for example, a new search engine or transcriber) in the `infrastructure/` layer.  
   - Update `services.yaml` and the DI container with the new service definition.

---

## Running Tests

This project uses pytest as its testing framework. A basic test scaffold has been set up.

To run the tests:

1. Ensure you have pytest installed in your environment. You can install it using:

   ```
   pip install pytest
   ```

2. From the root directory of the project, run:

   ```
   pytest
   ```

Note: If you encounter a "bad interpreter" error (e.g. "/opt/homebrew/bin/pytest: bad interpreter: /opt/homebrew/opt/python@3.11/bin/python3.11: no such file or directory"), please recreate your virtual environment by running:
   ```
   rm -rf venv
   python3 -m venv venv
   source ./venv/bin/activate
   pip install -r requirements.txt
   ```

All tests located in the `tests` directory will be automatically discovered and executed.

---

## Usage Examples (Detailed)

1. **Transcribe an Audio File**  
   `k transcribe --path ~/recordings/todays_notes.wav`  
   This will produce a transcription for the audio file.

2. **Assimilate a Voice Memo**  
   `k assimilate --path ~/recordings/daily_update.wav`  
   This adds the transcribed memo into your daily note (for example, in Obsidian).

3. **Ask an AI Agent**  
   `k ask --agent_name search_agent --prompt "What's the weather like in San Francisco?"`  
   This sends the prompt to the specified agent. The agent’s response is printed to your console.

4. **Run Discord Bot**  
   `k run discord`  
   This starts the Discord bot. Ensure your environment variables contain your bot token.

---

## Configuration & Extending k

Refer to the sections above for detailed instructions on how to configure the project settings and extend functionality with new commands, agents, or services.

## Running the Application

After installation and configuration, you can run the CLI using:

```
k --help
```

This will display the available commands and usage instructions.

---

## Additional Information

For more details on the project architecture, dependency injection, and service configuration, please refer to the project documentation and inline comments within the source code.
