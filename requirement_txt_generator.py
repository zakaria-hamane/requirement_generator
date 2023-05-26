import ast
import os
import pkg_resources


def get_imports(filepath):
    with open(filepath, 'r') as file:
        tree = ast.parse(file.read())

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    return imports


def get_installed_version(package):
    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return 'Not installed'


def generate_requirements():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    python_files = [file for file in os.listdir(script_dir) if file.endswith('.py')]

    requirements = set()
    for python_file in python_files:
        filepath = os.path.join(script_dir, python_file)
        imports = get_imports(filepath)
        for library in imports:
            version = get_installed_version(library)
            requirements.add(f"{library}=={version}")

    with open('requirements.txt', 'w') as file:
        file.write('\n'.join(sorted(requirements)))

    print("requirements.txt file generated successfully!")


generate_requirements()
