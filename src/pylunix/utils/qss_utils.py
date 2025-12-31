import re
from pathlib import Path
from typing import Dict

class QSSProcessor:
    def __init__(self, variables: dict = None):
        self.variables = variables or {}
        
        self._template_cache: Dict[str, str] = {}
        self._processed_cache: Dict[str, str] = {}
        self._compile_pattern()

    def set_variables(self, variables: dict):
        self.variables = variables
        self._compile_pattern()
        self._processed_cache.clear()

    def _compile_pattern(self):
        if not self.variables:
            self._pattern = None
            return
        keys = sorted(self.variables.keys(), key=len, reverse=True)
        escaped = [re.escape(k) for k in keys]
        pattern = r'(?<![A-Za-z0-9_])(?:' + '|'.join(escaped) + r')(?![A-Za-z0-9_])'
        self._pattern = re.compile(pattern)

    def _read_template(self, qss_path: str) -> str:
        if qss_path in self._template_cache:
            return self._template_cache[qss_path]

        path = Path(qss_path)
        if not path.exists():
            raise FileNotFoundError(f"QSS file not found: {qss_path}")
        
        content = path.read_text(encoding="utf-8")
        self._template_cache[qss_path] = content
        return content

    def apply_to_string(self, qss_content: str) -> str:
        if not self._pattern:
            return qss_content

        def _repl(m):
            key = m.group(0)
            return str(self.variables.get(key, key))
        return self._pattern.sub(_repl, qss_content)

    def get_processed_stylesheet(self, qss_path: str) -> str:
        if qss_path in self._processed_cache:
            return self._processed_cache[qss_path]

        template_content = self._read_template(qss_path)
        processed_content = self.apply_to_string(template_content)
        self._processed_cache[qss_path] = processed_content
        
        return processed_content

    def apply_to_file(self, qss_path: str) -> str:
        return self.get_processed_stylesheet(qss_path)

    def apply_to_files(self, qss_paths: list[str]) -> str:
        contents = []
        for path in qss_paths:
            contents.append(self.get_processed_stylesheet(path))
        return "\n".join(contents)