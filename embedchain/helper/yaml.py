import json
import logging
from typing import Dict

import yaml


def sanitize(data: Dict[str, str]) -> Dict[str, str]:
    """
    Optimize for human use by removing parts that are:
    1. duplicates
    2. hard to read
    3. redundant

    :param data: serialized json data
    :type data: Dict[str, str]
    :return: sanitized serialized json data
    :rtype: Dict[str, str]
    """
    # Session id should not be stored persistently
    del data["s_id"]
    # unique id is already stored persistently
    del data["u_id"]

    # If there's only one kind of config, there's no need to name the class
    del data["llm"]["config"]["__class__"]
    del data["embedder"]["config"]["__class__"]
    # db has separate configs, so the class matters.

    # Database references the sibling embedder class. This can be removed
    del data["db"]["embedder"]

    # Collection is a database attribute. The app attribute is deprecated.
    del data["config"]["collection_name"]

    # There's only one app type.
    del data["__class__"]

    # All remaining attributes are moved into 'session'
    keys_to_delete = []
    data["session"] = {}
    for key, value in data.items():
        if not isinstance(value, dict):
            data["session"][key] = value
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del data[key]

    # Delete session if it remained empty
    if data["session"] == {}:
        del data["session"]

    # Return dict
    return data


class Yaml:
    def save(self, filename: str = "config.yaml"):
        """
        Save the current state of the app to a reusable YAML file, where you can change config options.

        :param filename: path for the generated yaml file, defaults to "config.yaml"
        :type filename: str, optional
        """
        data = json.loads(self.serialize())

        # Sanitize
        sanitized_data = sanitize(data)

        with open(filename, "w") as file:
            yaml.dump(sanitized_data, file, default_flow_style=False)

        logging.info(f"Saved config to {filename}")

    @staticmethod
    def generate_default_config():
        """
        Generate a default yaml config in your file system,
        which you can adapt to your needs.

        example: `from embedchain import App; App.generate_default_config()`
        """
        from embedchain import App

        App().save()