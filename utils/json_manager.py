import json
import logging
from typing import Any, Optional

import aiofiles


class JSONManager(object):

    async def read(self, path: str) -> dict[str, Any]:
        """
        Reads a JSON file from the specified path.

        Args:
            path (str): The path to JSON file.

        Returns:
            dict: The contents of the JSON file as a dictionary.
        """
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            return self.to_json(content)

    async def write(self, path: str, new_data: dict[str, Any]) -> None:
        """
        Writes the given data to the specified JSON file.

        Args:
            path (str): The path to JSON file.
            new_data (dict): The data to write to the file, as a dictionary.
        """
        async with aiofiles.open(path, "r+", encoding="utf-8") as f:
            indent = 4
            await f.truncate()
            await f.seek(0)
            await f.write(self.to_string(new_data, indent=indent))

    @staticmethod
    def set(any_dict: dict[str, Any], module_path: str | list[str] | tuple[str], new_data: Any) -> None:
        """
        Update the data of a key in the given dictionary.

        Args:
            any_dict (dict): The dictionary that needs to be updated.
            module_path (str, list or tuple): The path to the key to be updated. It can take a list of keys as a string or a string with keys separated by a dot.
            new_data (Any): The new data to replace the key with.

        Returns:
            None
        """
        if not module_path:
            return

        if isinstance(module_path, str):
            module_path: list[str] = module_path.split(".")

        try:
            for key in module_path[:-1]:
                any_dict = any_dict.setdefault(key, {})

            any_dict[module_path[-1]] = new_data
        except (KeyError, TypeError, AttributeError) as e:
            logging.info(f"Failed to set data in %s: %s", module_path, e)

    @staticmethod
    def get(
        any_dict: dict[str, Any], module_path: str | list[str] | tuple[str]
    ) -> Optional[dict[str, Any]]:
        """
        Get the data of a key in the given dictionary.

        Args:
            any_dict (dict): The dictionary from which the data is to be retrieved.
            module_path (str or list): The path to the key to be retrieved. It can take a list of keys as a string or a string with keys separated by a dot.

        Returns:
            The data of the key in the dictionary.

            None, if the path was not provided in *module_path* or something went wrong.
        """

        if not module_path:
            return None

        if isinstance(module_path, str):
            module_path = module_path.split(".")

        try:
            new_data: dict[str, Any] = any_dict.copy()
            for key in module_path:
                new_data = new_data[key]
            return new_data
        except (KeyError, TypeError, AttributeError) as e:
            return logging.info(f"Failed to get data from %s: %s", module_path, e)

    @staticmethod
    def delete(any_dict: dict[str, Any], module_path: str | list[str] | tuple[str]) -> None:
        """
        Deletes data from a key in the given dictionary.

        Args:
            any_dict (dict): The dictionary from which the data is to be deleted.
            module_path (str or list): The path to the key to be deleted. It can take a list of keys as a string or a string with keys separated by a dot.

        Returns:
            None
        """

        if not module_path:
            return None

        if isinstance(module_path, str):
            module_path = module_path.split(".")

        try:
            for key in module_path[:-1]:
                any_dict = any_dict.setdefault(key, {})

            del any_dict[module_path[-1]]
        except (KeyError, TypeError, AttributeError) as e:
            logging.info(f"Failed to delete data from %s: %s", module_path, e)

    @staticmethod
    def to_json(data: str | bytes | bytearray) -> dict[str, Any]:
        """Formatting a string into a dict object"""
        return json.loads(data)

    @staticmethod
    def to_string(data: Any, indent: Optional[int] = None, ensure_ascii: Optional[bool] = False) -> str:
        """Format an object to a string"""
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
