import importlib
import pkgutil

def load_llm_plugins():
    package_name = "llm"

    for module_info in pkgutil.iter_modules(["llm"]):
        module_name = module_info.name

        # skip base modules
        if module_name in ["base", "registry", "factory", "loader"]:
            continue

        importlib.import_module(f"{package_name}.{module_name}")