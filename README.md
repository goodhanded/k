# k

**k** is a personal command-line interface (CLI) tool designed to streamline development workflows. It empowers you to generate pull request changesets, receive actionable code advice, create comprehensive project plans from user stories, and build troubleshooting prompts from tracebacks. Built on Clean Architecture principles, k leverages dependency injection to maintain a modular and extensible codebase.

---

## Table of Contents

- [k](#k)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Commands Overview](#commands-overview)
    - [Examples](#examples)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
  - [Extending k](#extending-k)
  - [Workflow Format](#workflow-format)
  - [Running Tests](#running-tests)
  - [Additional Information](#additional-information)
  - [Using k to update itself](#using-k-to-update-itself)

---

## Features

- **Pull Request Generation**: Generate detailed changesets based on your code modifications.
- **Code Advice**: Receive actionable suggestions and insights to improve your code.
- **Project Plan Generation**: Create comprehensive user stories and a project plan from a specified goal.
- **Troubleshooting Prompt**: Build a troubleshooting prompt from clipboard tracebacks, incorporating relevant source code excerpts.
- **.k Initialization**: Set up a project-specific .k directory with default configuration templates.
- **Changeset Implementation**: Apply structured changesets (additions, modifications, removals) from the clipboard to your project.

---

## Requirements

- **Python 3.8+** (Ensure you have a compatible version installed.)
- Pipenv or virtualenv (recommended) for Python dependency management
- Set the `K_PATH` environment variable to the absolute path of the project root for proper resolution of configuration files and templates.

---

## Installation

1. **Clone the Repository:**
   - `git clone https://github.com/goodhanded/k.git`
   - `cd k`

2. **Create and Activate a Virtual Environment:**
   - `python -m venv venv` (from project root)
   - `. ./venv/bin/activate`

3. **Install Dependencies:**
   - `pip install -r requirements.txt`

4. **(Optional) Set Up Environment Variables:**
   - Depending on the integrations you plan to use (OpenAI, AWS), you may need to set environment variables such as `OPENAI_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, etc.
   - **IMPORTANT:** Set the `K_PATH` environment variable to the absolute path of the project root directory. For example, add the following line to your shell configuration file (e.g., `.bashrc` or `.zshrc`):
     
     export K_PATH="/absolute/path/to/k"
     
   - Copy `.env.example` to `.env` and configure the variables for local development.

5. **Add Bash/Zsh Alias:**
   - In your shell configuration file (e.g., `.zshrc`), add:
     `alias k='/path/to/k/venv/bin/python /path/to/k/k.py'`
   - Now you can simply call `k` instead of `python k.py`

6. **Initialize the .k Directory:**
   - Run `k init` to create a fresh .k directory with default configuration templates. This is now required before using k in order to support commands being run from anywhere inside a project's subdirectories.

7. **Run the CLI:**
   - `k --help`

---

## Usage

All commands are defined in `commands.yaml`. To run a command, use:
`k <command> [args...]`

For subcommands:
`k <command> <subcommand> [args...]`

### Commands Overview

| Command      | Usage Example                                                                                                                  | Description |
|--------------|--------------------------------------------------------------------------------------------------------------------------------|-------------|
| **init**     | `k init`                                                                                                                       | Initializes the .k directory with default configuration templates. |
| **get**      | `k get openai models` <br> `k get anthropic models`                                                                              | Retrieves a list of available models from OpenAI or Anthropic. |
| **traceback**| `k traceback`                                                                                                                  | Builds a troubleshooting prompt from a traceback present in the clipboard, including source excerpts. |
| **pr**       | `k pr [prompt] [--copy] [--paste] [--include "<pattern>"] [--followup] [--verbose]`                                           | Generates a pull request changeset based on your modifications. Use the `--include` option to override the default file selection by providing a pipe-delimited list of glob patterns (e.g., '*.yaml|*.json|*.html'). Use the **--followup** flag to append this invocation's prompt and response to a memory file for incremental updates. The **--verbose** flag provides detailed debug output during execution. |
| **advise**   | `k advise "Refactor authentication module." [--followup] [--verbose]`                                                | Provides detailed code advice and suggestions for improvements. Use the **--followup** flag to append this invocation's prompt and response to a memory file for incremental updates. The **--verbose** flag enables verbose debug output. |
| **plan**     | `k plan [prompt] [--copy] [--verbose]`                                                                                           | Creates a project plan by generating user stories from the provided goal. The **--verbose** flag can be used to view detailed execution logs. |
| **implement**| `k implement [--verbose]`                                                                                                    | Implements a structured changeset read from the clipboard. The **--verbose** flag enables detailed debug output. |

---

### Examples

1. **Initialize .k Directory**  
   `k init`  
   Creates a new .k directory with default templates.

2. **Generate a Pull Request Changeset**  
   `k pr "Refactor database connection logic" --verbose`  
   Generates a detailed pull request changeset. Use the **--include** flag to override the default file selection if needed and the **--followup** flag to enable incremental updates. The **--verbose** flag displays detailed debug output.

3. **Generate Code Advice**  
   `k advise "Optimize the caching mechanism for performance." --followup --verbose`  
   Receives actionable code improvement suggestions. The **--followup** flag activates memory incorporation from previous sessions, while the **--verbose** flag enables detailed debug output.

4. **Generate a Project Plan**  
   `k plan "Implement user authentication" --copy --verbose`  
   Generates and optionally copies a detailed project plan comprising user stories. The **--verbose** flag provides extra execution details.

5. **Build a Troubleshooting Prompt**  
   Copy a traceback to your clipboard, then run:  
   `k traceback`  
   Constructs a troubleshooting prompt that includes relevant file content and the original traceback.

6. **Enable Verbose Output**  
   Simply add the **--verbose** flag to any command (e.g., `k pr "Refactor database connection logic" --verbose`) to display detailed debug output during execution.

7. **Implement Changeset from Clipboard**
   Copy a valid JSON changeset (like the one generated by `k pr`) to your clipboard, then run:
   `k implement --verbose`
   This command reads the changeset from the clipboard and applies the file additions, modifications, and removals to your project. Use the **--verbose** flag for detailed output.

---

## Configuration

- **K_PATH Environment Variable**  
  Ensure that the `K_PATH` environment variable is set to the absolute path of the project root directory. This variable is critical for proper resolution of configuration files like `.env`, `commands.yaml`, and `services.yaml`.

- **Application-wide Settings**  
  Configured via the `.env` file, which is read by `application/config` and injected into service constructors via the dependency injection container in `infrastructure/di`.

### Environment Variables

The application uses several environment variables which must be defined in your `.env` file. You can create your own `.env` by copying `.env.example` and modifying the values as needed:

- `K_PATH`: The root directory of the project.
- `OPENAI_API_KEY`: API key for accessing OpenAI's GPT models.
- `ANTHROPIC_API_KEY`: API key for accessing Anthropic's Claude models.

---

## Extending k

1. **Add a New Python Dependency**
   - Update `requirements.in` with the new dependency.
   - Run `pip-compile requirements.in --strip-extras` to update `requirements.txt`.
   - Install with `pip install -r requirements.txt`.

2. **Add a New Command**
   - Create or update a use case in the appropriate `application/...` folder.
   - Reference this use case in `commands.yaml` by specifying a target (e.g., `@agency.some_use_case.execute`).

3. **Add a New Service**
   - Create the service class (e.g., a new data processor or integration) in the `infrastructure/` layer.
   - Update `services.yaml` and register the service in the dependency injection container.

4. **Add a New Workflow**
   - Define a new workflow in `workflows.yaml` using the declarative edge notation.
   - Ensure that all node aliases used are registered in `services.yaml`.
   - Register the workflow in `services.yaml` using the Workflow Factory.
   - Update unit tests to validate the new workflow.

---

## Workflow Format

Workflows in k are defined in `workflows.yaml` and now support a hybrid format that combines the simplicity of concise edge notation with the flexibility of verbose conditional transitions. In its simplest form, a workflow is represented as an ordered list of transitions using the format:

```
FROM_NODE -> TO_NODE
```

Special tokens `START` and `END` denote the beginning and termination of a workflow. For example, a basic pull request workflow is defined as:

```
pull_request:
  - START -> get_project_path
  - get_project_path -> load_include_exclude_rules
  - get_project_path -> load_project_rules
  - load_project_rules -> load_file_collection
  - load_include_exclude_rules -> load_file_collection
  - load_file_collection -> load_directory_tree
  - load_file_collection -> load_source_code
  - load_directory_tree -> generate_changeset
  - load_source_code -> generate_changeset
  - generate_changeset -> record_memory
  - record_memory -> implement_changeset
  - implement_changeset -> END
```

To support dynamic routing based on state, you can also define transitions with conditions. In this verbose notation, an edge is specified as a mapping with the keys `from`, `to`, and `condition`. For instance:

```
hybrid_workflow:
  - START -> node_a
  - node_a -> 
      to: node_b
      condition: "state.some_condition == true"
  - node_a -> 
      to: END
      condition: "state.some_condition != true"
```

In a hybrid workflow, both concise and verbose edge definitions can be mixed together. Ensure that every node alias referenced is registered in `services.yaml` and that your workflow state includes any variables used in the conditions.

---

## Running Tests

This project uses pytest as its testing framework.

1. Ensure pytest is installed:
   ```
   pip install pytest
   ```

2. Run tests from the project root:
   ```
   pytest
   ```

All tests in the `tests` directory will be automatically discovered and executed.

---

## Additional Information

For details on the project architecture, dependency injection, and service configuration, refer to the inline comments in the source code.

---

## Using k to update itself

If you encounter issues updating k:

1. Create a work-in-progress (WIP) branch and commit your changes.
2. Switch back to the main branch.
3. In a separate clone of the repository (e.g., in a directory named `k-working`), pull the WIP branch.
4. Use the stable main branch to incrementally update the k-working project.

This approach ensures continuous progress even if intermittent issues arise.

---

Happy Coding!
