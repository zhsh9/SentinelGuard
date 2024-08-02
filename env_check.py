import subprocess
import sys
import os

def check_python_version():
    print("Checking Python version...")
    try:
        output = subprocess.check_output([sys.executable, "--version"], stderr=subprocess.STDOUT)
        print(output.decode().strip())
    except subprocess.CalledProcessError as e:
        print(f"Error checking Python version: {e.output.decode()}")
        return False
    return True

def parse_pip_list_output(output):
    """Parse pip list output to get a dictionary of package names and versions."""
    packages = {}
    for line in output.splitlines()[2:]:  # Skip the header lines
        name, version = line.split()[:2]
        packages[name] = version
    return packages

def check_python_dependencies():
    print("Checking Python dependencies...")
    try:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_file = os.path.join(cur_dir, "backend/requirements.txt")
        with open(requirements_file, "r") as f:
            requirements = f.read().splitlines()
        installed_output = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode()
        installed_packages = parse_pip_list_output(installed_output)
        
        # print(f"Installed packages: {installed_packages}")  # Print installed packages for debugging
        
        missing = []
        for req in requirements:
            if "==" in req:
                name, version = req.split("==")
                if name not in installed_packages or installed_packages[name] != version:
                    missing.append(req)
            else:
                if req not in installed_packages:
                    missing.append(req)

        if missing:
            print(f"Missing Python dependencies: {', '.join(missing)}")
            return False
        print("All Python dependencies are installed.")
    except Exception as e:
        print(f"Error checking Python dependencies: {e}")
        return False
    return True

def check_node_version():
    print("Checking Node.js version...")
    try:
        output = subprocess.check_output(["node", "--version"], stderr=subprocess.STDOUT)
        print(f"Node.js {output.decode().strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking Node.js version: {e.output.decode()}")
        return False
    return True

def check_npm_version():
    print("Checking npm version...")
    try:
        output = subprocess.check_output(["npm", "--version"], stderr=subprocess.STDOUT)
        print(f"npm {output.decode().strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking npm version: {e.output.decode()}")
        return False
    return True

def check_vue_dependencies():
    print("Checking Vue dependencies...")
    try:
        with open("frontend/package.json", "r") as f:
            import json
            package_json = json.load(f)
            dependencies = package_json.get("dependencies", {}).keys()
            dev_dependencies = package_json.get("devDependencies", {}).keys()
        
        result = subprocess.run(["npm", "list", "--depth=0"], cwd="frontend", capture_output=True, text=True)
        if result.returncode != 0:
            print(f"npm list output:\n{result.stdout}")
            print(f"npm list errors:\n{result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)
        
        installed = result.stdout
        missing = [dep for dep in list(dependencies) + list(dev_dependencies) if dep not in installed]
        if missing:
            print(f"Missing Vue dependencies: {', '.join(missing)}")
            return False
        print("All Vue dependencies are installed.")
    except Exception as e:
        print(f"Error checking Vue dependencies: {e}")
        return False
    return True

def main():
    python_ready = check_python_version() and check_python_dependencies()
    vue_ready = check_node_version() and check_npm_version() and check_vue_dependencies()
    
    if python_ready and vue_ready:
        print("All environments are ready.")
    else:
        print("Some environments are not ready. Please check the above logs for more details.")

if __name__ == "__main__":
    main()
