# AutoGen connector (scaffold)

This folder contains a minimal scaffold to integrate the AutoGen agent
orchestration runtime into this monorepo. It is intentionally lightweight
so you can opt-in when you want to run multi-agent flows locally or in a
controlled environment.

Why AutoGen?
- **Agent orchestration focus:** AutoGen is designed for coordinating
  multi-agent conversations and tool use, which aligns well with the
  goals of this project (orchestrating agents across connectors).
- **Flexible runtime:** It supports both local and remote execution,
  letting you prototype without heavy infra changes.
- **Good interoperability:** AutoGen can be used with existing LLM
  connectors (for example the OpenAI client in `connectors/openai`).

Quick start
1. Create/activate the Python virtualenv for `backend/`.
2. Install AutoGen (optional):

```bash
pip install autogen
```

3. Use the helper:

```py
from connectors.autogen.autogen_client import is_available, demo_info, generate_example_snippet

print(demo_info())
print(generate_example_snippet())
```

Notes
- The `autogen_client.py` file is a safe scaffold — it will import cleanly
  even if `autogen` is not installed. Once you install `autogen`, replace
  the template snippet with real orchestration code guided by AutoGen's
  documentation.
- This connector deliberately avoids hard dependencies in the main
  `requirements.txt`; installation is opt-in.

Integration ideas
- Use the existing `connectors/openai/openai_client.py` for model access
  and provide it as a Tool to AutoGen agents.
- Provide sample orchestration scripts under `backend/app/agents/` that
  implement common patterns (routing, tool use, memory access).
