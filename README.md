# 🧠 AI-Powered Self-Healing Test Automation Engine

This project is an advanced **SDET** Proof of Concept designed to eliminate the "Fragile Locator" problem in test automation. By wrapping the Selenium WebDriver with a **Local LLM (Llama 3.2)**, this engine autonomously repairs broken selectors in real-time.

## 🚀 Why Local AI (Ollama + Llama 3.2)?
Reflecting the high security and privacy standards required for big companies, this project adopts a **Local LLM strategy**:

* **GDPR Compliance:** No DOM data or proprietary code is sent to external cloud providers.
* **Security:** 100% of the analysis happens within the local infrastructure.
* **Cost-Efficiency:** No API token costs or external dependencies for the healing process.
* **Performance:** Integrated with a **Smart Cache** layer to ensure subsequent runs take less than 2 seconds.

## 🏗️ Architecture
The framework utilizes a **Side-by-Side Architecture**, isolating the **System Under Test (SUT)** from the **Automation Engine** to ensure modularity and scalability.



### Key Components:
* **SUT (Django):** A real-world authentication system with intentional UI mutations (V1 vs V2).
* **Healing Driver (Proxy/Wrapper):** A custom Selenium implementation that intercepts `NoSuchElementException`.
* **LLM Engine:** A specialized module using **Few-Shot Prompting** for precise DOM analysis via Ollama.
* **Smart Cache:** A persistent JSON layer that memorizes healed locators.

## 🛠️ Project Structure
```text
.
├── sut_django_app/          # The System Under Test (Django)
└── qa_automation_engine/    # The AI-Powered Testing Framework
    ├── core/                # Healing Logic & LLM Engine
    ├── tests/               # Pytest Test Suites
    └── cache/               # Persistence Layer (Healed Locators)
```

## 🚥 How to Run

### 1. Prerequisites
* **Python 3.13+**: Ensure your environment is up to date.
* **Ollama**: Must be installed and running in the background.
* **Llama 3.2 Model**: Pull and run the model locally using `ollama run llama3.2`.

### 2. Start the System Under Test (SUT)
Navigate to the application folder and initialize the Django server:

```bash
cd sut_django_app
python manage.py migrate
python manage.py runserver
```

> **Environment Note**: The application will be accessible at `http://127.0.0.1:8000/login/v2/`. This version contains mutated locators specifically designed to trigger the AI-healing logic.

### 3. Run the Self-Healing Tests
Open a **second terminal** and navigate to the framework folder to execute the AI-driven test suite:

```bash
# Navigate to the automation engine root
cd qa_automation_engine

# Run the test suite 
python -m pytest tests/test_login.py -s -v 
```

## 📊 Execution Results & ROI

During the execution, the framework demonstrates its resilience by intercepting locator failures caused by UI mutations in the SUT (System Under Test).

### Initial Execution (The Healing Process)
- **Detection**: The `HealingDriver` intercepts a `NoSuchElementException`.
- **Analysis**: The **Llama 3.2** model analyzes the DOM and suggests a new valid locator.
- **Recovery**: The test resumes automatically without manual intervention.
- **Duration**: ~40-60 seconds (including LLM inference time).

### Subsequent Executions (The Optimization)
- **Persistence**: The healed locator is retrieved from the **Smart Cache**.
- **Performance**: The test runs at native Selenium speed.
- **Duration**: < 2 seconds for the login flow.

## 💾 Intelligence Persistence (Smart Cache)

One of the core features of this engine is the **Smart Cache System**. When the AI successfully heals a locator, the framework does not discard that knowledge. Instead, it serializes the discovery into a persistent state.

### How it works:
1. **Discovery**: Upon a successful healing, the engine maps the broken locator to the new one.
2. **Serialization**: The framework automatically creates/updates a `healed_locators.json` file inside the `qa_automation_engine/cache/` directory.
3. **Efficiency**: On the next run, the `HealingDriver` checks the JSON first, bypassing the LLM inference and executing at native speed.

### The Generated Artifact:
The system produces a structured JSON like the one below:

```json
{
    "id:login-username": {
        "by": "name",
        "value": "user_id_input"
    },
    "id:login-password": {
        "by": "name",
        "value": "user_pwd_input"
    },
    "id:btn-submit-login": {
        "by": "css selector",
        "value": ".btn-login-submit"
    }
}
