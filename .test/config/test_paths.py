from pylunix.config.path import BASE_DIR, RESOURCES_DIR, COMMON_DIR, COMPONENTS_DIR, COMMON_THEME_YAML, component_yaml_path

print("BASE_DIR:", BASE_DIR)
print("RESOURCES_DIR:", RESOURCES_DIR)
print("COMMON_DIR:", COMMON_DIR)
print("COMPONENTS_DIR:", COMPONENTS_DIR)
print("COMMON_THEME_YAML:", COMMON_THEME_YAML)

# 測試 component_yaml_path
component_name = "button"
yaml_path = component_yaml_path(component_name)
print(f"YAML path for '{component_name}': {yaml_path}")

# 檢查路徑是否存在（可選）
print("COMMON_THEME_YAML exists?", COMMON_THEME_YAML.exists())
print(f"{yaml_path} exists?", yaml_path.exists())
