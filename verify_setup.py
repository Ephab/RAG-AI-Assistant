import sys
import subprocess

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    print("\nChecking dependencies...")

    packages = {
        'pymupdf4llm': 'pymupdf4llm',
        'requests': 'requests',
        'tqdm': 'tqdm',
        'chromadb': 'chromadb',
        'sentence_transformers': 'sentence-transformers',
        'tiktoken': 'tiktoken'
    }

    all_installed = True
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} (Not installed)")
            all_installed = False

    return all_installed

def check_ollama():
    print("\nChecking Ollama...")

    try:
        result = subprocess.run(['ollama', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"Ollama installed: {result.stdout.strip()}")
        else:
            print("Ollama not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("Ollama not found in PATH")
        print("Install from: https://ollama.ai")
        return False

    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=3)
        if response.status_code == 200:
            print("Ollama service is running")

            # check if llama3.2 model is available
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]

            if any('llama3.2' in name for name in model_names):
                print("llama3.2 model available")
            else:
                print("llama3.2 model not found")
                print("Run: ollama pull llama3.2")
                return False
        else:
            print("Ollama service not responding")
            return False
    except Exception as e:
        print(f"Cannot connect to Ollama service")
        print(f"Run: ollama serve")
        return False

    return True

def main():
    print("RAG PDF Assistant Setup Verification")

    results = []

    results.append(check_python_version())
    results.append(check_dependencies())
    results.append(check_ollama())

    if all(results):
        print("All checks passed! You're ready to run the assistant.")
        print("\nRun: python main.py")
        return 0
    else:
        print("Some checks failed. Please fix the issues above.")
        print("\nInstall dependencies: pip install -r requirements.txt")
        print("Install Ollama: https://ollama.ai")
        return 1

if __name__ == "__main__":
    sys.exit(main())

