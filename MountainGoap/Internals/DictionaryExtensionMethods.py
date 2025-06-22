# // <copyright file="DictionaryExtensionMethods.py" company="Chris Muller">
# // Copyright (c) Chris Muller. All rights reserved.
# // </copyright>

from typing import Dict, Any, Optional, List
from ..ComparisonValuePair import ComparisonValuePair

class DictionaryExtensionMethods:
    """
    Extension method to copy a dictionary of strings and objects.
    In Python, this will be implemented as static methods since there are no true extension methods.
    """

    @staticmethod
    def copy_dict(dictionary: Dict[str, Optional[Any]]) -> Dict[str, Optional[Any]]:
        """
        Copies the dictionary to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    # In Python, standard dict is generally thread-safe for basic operations, and
    # for more complex concurrent updates, a Lock or queue would be used.
    # For a direct equivalent, we'll just use a standard dict copy.
    @staticmethod
    def copy_concurrent_dict(dictionary: Dict[str, Optional[Any]]) -> Dict[str, Optional[Any]]:
        """
        Copies the (conceptually) concurrent dictionary to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    @staticmethod
    def copy_comparison_value_pair_dict(dictionary: Dict[str, ComparisonValuePair]) -> Dict[str, ComparisonValuePair]:
        """
        Copies the dictionary of ComparisonValuePair to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    @staticmethod
    def copy_string_dict(dictionary: Dict[str, str]) -> Dict[str, str]:
        """
        Copies the dictionary of strings to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

    @staticmethod
    def copy_non_nullable_dict(dictionary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Copies the dictionary of non-nullable objects to a shallow clone.

        Args:
            dictionary: Dictionary to be copied.

        Returns:
            A shallow copy of the dictionary.
        """
        return dictionary.copy()

