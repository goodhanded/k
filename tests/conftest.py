import os
import sys

# Add the project root directory to sys.path so that imports for modules like 'infrastructure', 'adapters', 'domain', etc. work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
