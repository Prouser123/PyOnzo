from importlib import import_module
from os.path import dirname, basename, isfile, join
import glob


from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.clamp import ClampDevice
from mqtt.devices.display import DisplayDevice

class EntityLoader:
    def __init__(self, client: Client, scheduler: BackgroundScheduler, display_device: DisplayDevice, clamp_device: ClampDevice):
        self.__client = client
        self.__scheduler = scheduler
        self.__display_device = display_device
        self.__clamp_device = clamp_device
    
    def load(self):
        self.load_display_entities()
        self.load_clamp_entities()

    def load_clamp_entities(self):
        module, classes = self.__get_entities_in_folder("clamp")

        for c in classes:
            print(f"[EntityLoader.load.clamp] Instantiating class '{c}'")
            getattr(module, c)(self.__client, self.__scheduler, self.__clamp_device)

    def load_display_entities(self):
        module, classes = self.__get_entities_in_folder("display")
        
        for c in classes:
            print(f"[EntityLoader.load.display] Instantiating class '{c}'")
            getattr(module, c)(self.__client, self.__scheduler, self.__display_device)

    def __get_entities_in_folder(self, folder):
        # 1. Find .py files in folder
        # (src: https://stackoverflow.com/a/1057534)
        modules = glob.glob(f"{dirname(__file__)}/{folder}/*.py")
        __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
        
        # 2. Import the modules (.py files)
        for m in __all__:
            path = f"mqtt.homeassistant.entities.{folder}.{m}"
            print(f"[EntityLoader.import] Importing module '{path}'...")
            module = import_module(path)

            base_classes = ["ClampEntity", "DisplayEntity"]

            classes = [i for i in module.__dict__ if i.endswith("Entity") and i not in base_classes]

            print(f"[EntityLoader.import] Found classes: {', '.join(classes)}")
            # Found classes: Class1, Class2

            return module, classes
