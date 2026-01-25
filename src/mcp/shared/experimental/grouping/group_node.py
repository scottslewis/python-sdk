from typing import List, Optional, Callable, Any, Self
from threading import Lock
from mcp.shared.experimental.grouping.base_node import BaseNode
from mcp.shared.experimental.grouping.tool_node import ToolNode
from mcp.shared.experimental.grouping.resource_node import ResourceNode
from mcp.shared.experimental.grouping.prompt_node import PromptNode

class GroupNode(BaseNode):
    """
    GroupNode class that extends BaseNode functionality.
    Represents a group node in a hierarchical tree structure that can contain
    child groups, tools, prompts, and resources.
    """
    
    # Class constant
    DEFAULT_SEPARATOR = "."
    
    def __init__(self, name: str, name_separator: Optional[str] = None):
        """
        Initialize a GroupNode with the given name and optional separator.
        
        Args:
            name: The name of the group node (must not be None)
            name_separator: The separator for fully qualified names (default: DEFAULT_SEPARATOR)
        """
        # Validate name is not None (equivalent to Objects.requireNonNull)
        if name is None:
            raise ValueError("name must not be null")
        
        # Initialize BaseNode attributes
        self.name = name
        self.name_separator = name_separator if name_separator is not None else self.DEFAULT_SEPARATOR
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.meta: Optional[dict] = None
        
        # Initialize GroupNode specific attributes
        self._parent: Optional['GroupNode'] = None
        
        # Initialize child lists (CopyOnWriteArrayList equivalent with locks)
        self._child_groups: List['GroupNode'] = []
        self._child_tools: List['ToolNode'] = []
        self._child_prompts: List['PromptNode'] = []
        self._child_resources: List['ResourceNode'] = []
        
        # Initialize locks for thread-safe operations
        self._child_groups_lock = Lock()
        self._child_tools_lock = Lock()
        self._child_prompts_lock = Lock()
        self._child_resources_lock = Lock()
        
        # Converter function
        self._converter: Optional[Callable[['GroupNode'], Any]] = None
    
    # BaseNode methods
    def get_name(self) -> str:
        """Get the name of this node."""
        return self.name
    
    def get_title(self) -> Optional[str]:
        """Get the title of this node."""
        return self.title
    
    def set_title(self, title: str) -> None:
        """Set the title of this node."""
        self.title = title
    
    def get_description(self) -> Optional[str]:
        """Get the description of this node."""
        return self.description
    
    def set_description(self, description: str) -> None:
        """Set the description of this node."""
        self.description = description
    
    def get_meta(self) -> Optional[dict]:
        """Get the metadata dictionary of this node."""
        return self.meta
    
    def set_meta(self, meta: dict) -> None:
        """Set the metadata dictionary of this node."""
        self.meta = meta
    
    def __hash__(self) -> int:
        """Return hash code based on the name."""
        return hash(self.name) if self.name is not None else 0
    
    def __eq__(self, obj: Any) -> bool:
        """
        Check equality based on the name and class type.
        
        Args:
            obj: The object to compare with
            
        Returns:
            True if objects are equal, False otherwise
        """
        if self is obj:
            return True
        if obj is None:
            return False
        if type(self) != type(obj):
            return False
        other = obj
        return self.name == other.name
    
    # GroupNode specific methods
    @property
    def parent(self) -> Optional['GroupNode']:
        """Get the parent GroupNode (property for direct access)."""
        return self._parent
    
    def get_parent(self) -> Optional['GroupNode']:
        """Get the parent GroupNode."""
        return self._parent
    
    def get_root(self) -> 'GroupNode':
        """
        Get the root GroupNode by traversing up the parent chain.
        
        Returns:
            The root GroupNode (the node with no parent)
        """
        parent = self._parent
        if parent is None:
            return self
        else:
            return parent.get_root()
    
    def is_root(self) -> bool:
        """
        Check if this node is a root node (has no parent).
        
        Returns:
            True if this is a root node, False otherwise
        """
        return self._parent is None
    
    def add_child_group(self, child_group: 'GroupNode') -> bool:
        """
        Add a child GroupNode to this group.
        
        Args:
            child_group: The GroupNode to add as a child
            
        Returns:
            True if the child was added successfully, False otherwise
        """
        with self._child_groups_lock:
            # Check if already in the list to mimic add behavior
            if child_group not in self._child_groups:
                self._child_groups.append(child_group)
                child_group._parent = self
                return True
            return False
    
    def remove_child_group(self, child_group: 'GroupNode') -> bool:
        """
        Remove a child GroupNode from this group.
        
        Args:
            child_group: The GroupNode to remove
            
        Returns:
            True if the child was removed successfully, False otherwise
        """
        with self._child_groups_lock:
            try:
                self._child_groups.remove(child_group)
                child_group._parent = None
                return True
            except ValueError:
                return False
    
    def get_children_groups(self) -> List[Self]:
        """
        Get the list of child GroupNodes.
        
        Returns:
            List of child GroupNodes
        """
        return self._child_groups
    
    def add_child_tool(self, child_tool: ToolNode) -> bool:
        """
        Add a child ToolNode to this group.
        
        Args:
            child_tool: The ToolNode to add as a child
            
        Returns:
            True if the child was added successfully, False otherwise
        """
        with self._child_tools_lock:
            # Check if already in the list to mimic add behavior
            if child_tool not in self._child_tools:
                self._child_tools.append(child_tool)
                child_tool.add_parent_group(self)
                return True
            return False
    
    def remove_child_tool(self, child_tool: ToolNode) -> bool:
        """
        Remove a child ToolNode from this group.
        
        Args:
            child_tool: The ToolNode to remove
            
        Returns:
            True if the child was removed successfully, False otherwise
        """
        with self._child_tools_lock:
            try:
                self._child_tools.remove(child_tool)
                child_tool.remove_parent_group(self)
                return True
            except ValueError:
                return False
    
    def get_children_tools(self) -> List[ToolNode]:
        """
        Get the list of child ToolNodes.
        
        Returns:
            List of child ToolNodes
        """
        return self._child_tools
    
    def add_child_prompt(self, child_prompt: PromptNode) -> bool:
        """
        Add a child PromptNode to this group.
        
        Args:
            child_prompt: The PromptNode to add as a child
            
        Returns:
            True if the child was added successfully, False otherwise
        """
        with self._child_prompts_lock:
            # Check if already in the list to mimic add behavior
            if child_prompt not in self._child_prompts:
                self._child_prompts.append(child_prompt)
                child_prompt.add_parent_group(self)
                return True
            return False
    
    def remove_child_prompt(self, child_prompt: PromptNode) -> bool:
        """
        Remove a child PromptNode from this group.
        
        Args:
            child_prompt: The PromptNode to remove
            
        Returns:
            True if the child was removed successfully, False otherwise
        """
        with self._child_prompts_lock:
            try:
                self._child_prompts.remove(child_prompt)
                child_prompt.remove_parent_group(self)
                return True
            except ValueError:
                return False
    
    def get_children_prompts(self) -> List[PromptNode]:
        """
        Get the list of child PromptNodes.
        
        Returns:
            List of child PromptNodes
        """
        return self._child_prompts
    
    def get_children_resources(self) -> List[ResourceNode]:
        """
        Get the list of child ResourceNodes.
        
        Returns:
            List of child ResourceNodes
        """
        return self._child_resources
    
    def add_child_resource(self, child_resource: ResourceNode) -> bool:
        """
        Add a child ResourceNode to this group.
        
        Args:
            child_resource: The ResourceNode to add as a child
            
        Returns:
            True if the child was added successfully, False otherwise
        """
        with self._child_resources_lock:
            # Check if already in the list to mimic add behavior
            if child_resource not in self._child_resources:
                self._child_resources.append(child_resource)
                child_resource.add_parent_group(self)
                return True
            return False
    
    def remove_child_resource(self, child_resource: ResourceNode) -> bool:
        """
        Remove a child ResourceNode from this group.
        Note: The original Java method is named 'removeChildPrompt' but operates on ResourceNode,
        which appears to be a typo. The Python version uses the correct name.
        
        Args:
            child_resource: The ResourceNode to remove
            
        Returns:
            True if the child was removed successfully, False otherwise
        """
        with self._child_resources_lock:
            try:
                self._child_resources.remove(child_resource)
                child_resource.remove_parent_group(self)
                return True
            except ValueError:
                return False
    
    def _get_fully_qualified_name_helper(self, sb: list, tg: Self) -> str:
        """
        Helper method to recursively build the fully qualified name.
        
        Args:
            sb: A list used as a string buffer (unused but kept for signature compatibility)
            tg: The target GroupNode to build the name for
            
        Returns:
            The fully qualified name of the target node
        """
        parent = tg.get_parent()
        if parent is not None:
            parent_name = self._get_fully_qualified_name_helper(sb, parent)
            return parent_name + self.name_separator + tg.get_name()
        return tg.get_name()
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name of this node by traversing the parent chain.
        
        Returns:
            The fully qualified name (e.g., "parent.child.grandchild")
        """
        return self._get_fully_qualified_name_helper([], self)
    
    def __str__(self) -> str:
        """
        Return a string representation of this GroupNode.
        
        Returns:
            String representation including all key attributes
        """
        return (f"GroupNode [name={self.name}, fqName={self.get_fully_qualified_name()}, "
                f"isRoot={self.is_root()}, title={self.title}, description={self.description}, "
                f"meta={self.meta}, childGroups={self._child_groups}, childTools={self._child_tools}, "
                f"childPrompts={self._child_prompts}]")


