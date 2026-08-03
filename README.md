# JARVIS V5

An AI-powered desktop assistant focused on conversational interaction, system control, command execution, and personal productivity.

> **Status:** Final Release (Archived)
>
> JARVIS V5 represents the final iteration of the V5 architecture. Development has now moved to **JARVIS V6**, a complete architectural redesign focused on modularity, long-term memory, event-driven systems, and extensibility.

---

## Features

- 💬 Natural conversational interface
- 🖥️ Operating system command execution
- 📁 File and directory operations
- ⏰ Task scheduling and reminders
- 🧠 Personal context handling
- 📅 Daily summary automation
- 🔧 Function calling pipeline
- 🌐 Internet connectivity checks
- 📝 JSON-based command generation

---

## Tech Stack

- Python
- Ollama
- Local LLMs
- JSON Function Calling
- Modular Python Architecture

---

## Project Structure

```
Driver/
advanced_utilities/
alert/
brain/
conscious_core/
daily_summary_automation/
function_calling/
internet_connectivity_check/
os_command_brain/
os_operations/
task_scheduler/
utils/
```

---

## Example

```
User:
Create a file named notes.txt on my Desktop.

JARVIS:
⚙️ Command

{
  "action": "create_file",
  "filename": "notes.txt",
  "location": "Desktop"
}
```

---

## Limitations

JARVIS V5 was built as an experimental architecture and has several limitations:

- Hard-coded workflows in multiple components
- Limited long-term memory
- Tight coupling between modules
- Basic tool orchestration
- No event-driven architecture
- Limited extensibility

These limitations are the primary motivation behind the development of **JARVIS V6**.

---

## Roadmap

This repository is considered complete.

Future development continues in **JARVIS V6**, featuring:

- Modular architecture
- Event Bus
- Planner-driven execution
- Persistent cognitive memory
- Plugin system
- Mission Control dashboard
- Advanced automation
- Local AI operating environment

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.