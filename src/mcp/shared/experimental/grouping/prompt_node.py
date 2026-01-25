from typing import List, Dict, Any, Optional
from mcp.shared.experimental.grouping.base_leaf_node import BaseLeafNode


class PromptNode(BaseLeafNode):
    """
    Python translation of PromptNode extending BaseLeafNode
    """
    
    def __init__(self, name: str):
        """
        Constructor that initializes the PromptNode with a name.
        
        Args:
            name: The name of the prompt node
        """
        # Call parent constructor
        if name is None:
            raise ValueError("name must not be null")
        
        # BaseNode fields
        self.name: str = name
        self._name_separator: str = "."  # DEFAULT_SEPARATOR
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.meta: Optional[Dict[str, Any]] = None
        
        # BaseLeafNode fields
        self._parent_groups: List = []  # List[GroupNode]
        
        # PromptNode fields
        self._prompt_arguments: List = []  # List[PromptArgumentNode] - thread-safe list simulation
    
    # BaseNode methods (inherited behavior)
    def get_name(self) -> str:
        """Get the name of the node"""
        return self.name
    
    def get_title(self) -> Optional[str]:
        """Get the title of the node"""
        return self.title
    
    def set_title(self, title: str) -> None:
        """Set the title of the node"""
        self.title = title
    
    def get_description(self) -> Optional[str]:
        """Get the description of the node"""
        return self.description
    
    def set_description(self, description: str) -> None:
        """Set the description of the node"""
        self.description = description
    
    def get_meta(self) -> Optional[Dict[str, Any]]:
        """Get the metadata dictionary"""
        return self.meta
    
    def set_meta(self, meta: Dict[str, Any]) -> None:
        """Set the metadata dictionary"""
        self.meta = meta
    
    def __hash__(self) -> int:
        """Hash code based on name"""
        return hash(self.name)
    
    def __eq__(self, obj) -> bool:
        """Equality comparison based on name"""
        if self is obj:
            return True
        if obj is None:
            return False
        if self.__class__ != obj.__class__:
            return False
        other = obj
        return self.name == other.name
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name.
        Overridden from BaseNode - BaseLeafNode implementation returns just the name
        """
        return self.name
    
    # BaseLeafNode methods (inherited behavior)
    def add_parent_group(self, parent_group) -> bool:
        """
        Add a parent group.
        
        Args:
            parent_group: The parent group to add (GroupNode)
            
        Returns:
            True if the parent group was added successfully
            
        Raises:
            ValueError: If parent_group is None
        """
        if parent_group is None:
            raise ValueError("parentGroup must not be null")
        self._parent_groups.append(parent_group)
        return True
    
    def remove_parent_group(self, parent_group) -> bool:
        """
        Remove a parent group.
        
        Args:
            parent_group: The parent group to remove (GroupNode)
            
        Returns:
            True if the parent group was removed successfully, False otherwise
        """
        try:
            self._parent_groups.remove(parent_group)
            return True
        except ValueError:
            return False
    
    def get_parent_groups(self) -> List:
        """
        Get the list of parent groups.
        
        Returns:
            List of parent groups (List[GroupNode])
        """
        return self._parent_groups
    
    def get_parent_group_roots(self) -> List:
        """
        Get the roots of all parent groups.
        
        Returns:
            List of parent group roots (List[GroupNode])
        """
        parent_groups = self._parent_groups
        return [group.get_root() for group in parent_groups]
    
    # PromptNode specific methods
    def get_prompt_arguments(self) -> List:
        """
        Get the list of prompt arguments.
        
        Returns:
            List of prompt arguments (List[PromptArgumentNode])
        """
        return self._prompt_arguments
    
    def add_prompt_argument(self, prompt_argument) -> bool:
        """
        Add a prompt argument to the list.
        
        Args:
            prompt_argument: The prompt argument to add (PromptArgumentNode)
            
        Returns:
            True if the prompt argument was added successfully
            
        Raises:
            ValueError: If prompt_argument is None
        """
        if prompt_argument is None:
            raise ValueError("promptArgument must not be null")
        self._prompt_arguments.append(prompt_argument)
        return True
     
    def __str__(self) -> str:
        """
        String representation of the PromptNode.
        Overrides Object.toString()
        
        Returns:
            String representation including all fields
        """
        return (f"PromptNode [promptArguments={self._prompt_arguments}, name={self.name}, "
                f"fqName={self.get_fully_qualified_name()}, title={self.title}, "
                f"description={self.description}, meta={self.meta}]")
