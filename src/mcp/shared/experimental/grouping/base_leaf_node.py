# base_leaf_node.py
from typing import List, Optional
from mcp.shared.experimental.grouping.base_node import BaseNode
from mcp.shared.experimental.grouping.group_node import GroupNode

class BaseLeafNode(BaseNode):
    """
    BaseLeafNode class representing a leaf node in the hierarchy.
    Extends BaseNode and manages parent group relationships.
    """

    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize a BaseLeafNode with the given name and optional separator.
        
        Args:
            name: The name of the leaf node
            name_separator: Optional separator for name formatting
        """
        if name_separator is not None:
            super().__init__(name, name_separator)
        else:
            super().__init__(name)
        self._parent_groups: List[GroupNode] = []

    def add_parent_group(self, parent_group: GroupNode) -> bool:
        """
        Add a parent group to this leaf node.
        
        Args:
            parent_group: The GroupNode to add as a parent
            
        Returns:
            True if the parent group was added successfully
            
        Raises:
            ValueError: If parent_group is None
        """
        if parent_group is None:
            raise ValueError("parentGroup must not be null")
        self._parent_groups.append(parent_group)
        return True

    def remove_parent_group(self, parent_group: GroupNode) -> bool:
        """
        Remove a parent group from this leaf node.
        
        Args:
            parent_group: The GroupNode to remove
            
        Returns:
            True if the parent group was removed, False otherwise
        """
        try:
            self._parent_groups.remove(parent_group)
            return True
        except ValueError:
            return False

    def get_parent_groups(self) -> List[GroupNode]:
        """
        Get the list of parent groups.
        
        Returns:
            List of parent GroupNodes
        """
        return self._parent_groups

    def get_parent_group_roots(self) -> List[GroupNode]:
        """
        Get the root nodes of all parent groups.
        
        Returns:
            List of root GroupNodes
        """
        parent_groups = self._parent_groups
        return [group.get_root() for group in parent_groups]

    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name of this leaf node.
        For leaf nodes, this is simply the name itself.
        
        Returns:
            The fully qualified name
        """
        return self._name


