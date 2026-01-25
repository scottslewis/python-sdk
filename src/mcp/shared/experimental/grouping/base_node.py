# base_node.py
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    Abstract base class for all nodes in the hierarchy.
    Provides common properties and methods for node management.
    """

    DEFAULT_SEPARATOR: str = "."

    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize a BaseNode with the given name and optional separator.
        
        Args:
            name: The name of the node
            name_separator: Optional separator for name formatting (defaults to DEFAULT_SEPARATOR)
            
        Raises:
            ValueError: If name is None
        """
        if name is None:
            raise ValueError("name must not be null")
        self._name: str = name
        self._name_separator: str = name_separator if name_separator is not None else self.DEFAULT_SEPARATOR
        self._title: Optional[str] = None
        self._description: Optional[str] = None
        self._meta: Optional[Dict[str, Any]] = None

    def get_name(self) -> str:
        """
        Get the name of the node.
        
        Returns:
            The node's name
        """
        return self._name

    def get_title(self) -> Optional[str]:
        """
        Get the title of the node.
        
        Returns:
            The node's title or None
        """
        return self._title

    def set_title(self, title: str) -> None:
        """
        Set the title of the node.
        
        Args:
            title: The title to set
        """
        self._title = title

    def get_description(self) -> Optional[str]:
        """
        Get the description of the node.
        
        Returns:
            The node's description or None
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Set the description of the node.
        
        Args:
            description: The description to set
        """
        self._description = description

    def get_meta(self) -> Optional[Dict[str, Any]]:
        """
        Get the metadata dictionary.
        
        Returns:
            The metadata dictionary or None
        """
        return self._meta

    def set_meta(self, meta: Dict[str, Any]) -> None:
        """
        Set the metadata dictionary.
        
        Args:
            meta: The metadata dictionary to set
        """
        self._meta = meta

    def __hash__(self) -> int:
        """
        Compute hash code based on the node's name.
        
        Returns:
            Hash value of the node
        """
        return hash(self._name)

    def __eq__(self, obj: object) -> bool:
        """
        Check equality based on node name and class type.
        
        Args:
            obj: Object to compare with
            
        Returns:
            True if objects are equal, False otherwise
        """
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        return self._name == other._name

    @abstractmethod
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name of the node.
        Must be implemented by subclasses.
        
        Returns:
            The fully qualified name
        """
        pass
