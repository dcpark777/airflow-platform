import os
import inspect
import pkgutil
import importlib
from maestro.maestro import maestro, Action

def get_classes(package_name: str): 
    # package_path = os.getcwd()  + f"/{'/'.join(package_name.split('.'))}"
    package_path = "/Users/danpark/Projects/airflow-platform/dags/plugins/operators"
    print(f"Getting packages from path: {package_path}")
    package_modules = [info for info in pkgutil.walk_packages([package_path], package_name + '.', onerror=print)]
    print(package_modules)

    maestro_classes = []
    for info in package_modules:
        print(f"Checking module: {info.name}")
        module = importlib.import_module(info.name)
        is_maestro = (
            lambda obj: obj.__module__.startswith(package_name)
            and hasattr(obj, 'maestro_meta')
            and not inspect.isabstract(obj)
        )
        module_maestro_classes = [obj for _, obj in inspect.getmembers(module, inspect.isclass) if is_maestro(obj)]
        print(f"Found maestro classes: {module_maestro_classes}")
        maestro_classes.extend(module_maestro_classes)
    return maestro_classes


def get_maestro_metadata(clazz) -> maestro:
    print(f"Extracting maestro metadata from class: {clazz.__name__}")
    try:
        maestro_meta: maestro = getattr(clazz, 'maestro_meta')
        print(f"Maestro meta: {maestro_meta}")
        return maestro_meta
    except Exception as e:
        print(f"Error getting maestro meta: {e}")
        return None


def build_action(clazz):
    print(f"Building action for class: {clazz.__name__}")
    maestro_meta: maestro = get_maestro_metadata(clazz)
    action_name: str = maestro_meta.action_name
    runs: str = clazz.__name__
    parameters = inspect.signature(clazz.__init__).parameters
    params = [p for p in parameters.keys() if p not in ['self', 'args', 'kwargs']]
    action = Action(action_name, runs, params)
    return action


def save_action(action: Action):
    print(f"Saving action: {action}")
    # save to database


if __name__ == "__main__":
    maestro_classes = get_classes('plugins.operators')
    print(f"Found all maestro classes: {maestro_classes}")

    for clazz in maestro_classes:
        maestro_metadata: maestro = get_maestro_metadata(clazz)
        if maestro_metadata is None:
            print(f"Skipping class: {clazz.__name__}. Reason: No maestro metadata")
            continue
        elif maestro_metadata.export == False:
            print(f"Skipping class: {clazz.__name__}. Reason: Export disabled")
            continue
        else: # process metadata
            action = build_action(clazz)
            save_action(action)
            
        # print(f"Action: {action}")
        # clazz_instance = clazz()
        # clazz_instance.execute(None)
