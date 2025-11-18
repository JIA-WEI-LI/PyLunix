# paths.py
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# resources
RESOURCES_DIR = BASE_DIR / "resources"
COMMON_DIR = BASE_DIR / "common"
COMPONENTS_DIR = BASE_DIR / "components"
CONTROLS_DIR = BASE_DIR / "components" / "controls"

# theme YAML
COMMON_THEME_YAML = RESOURCES_DIR / "common_themeresources_any.yaml"

def component_yaml_path(component_dir: str, component_name: str) -> Path:
    return COMPONENTS_DIR / component_dir / component_name / f"{component_name}.yaml"

def component_qss_path(component_dir: str, component_name: str) -> Path:
    return COMPONENTS_DIR / component_dir / component_name / f"{component_name}.qss"