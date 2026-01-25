from mcp.shared.experimental.grouping.base_node import BaseNode

class PromptArgumentNode(BaseNode):
    """
    A node representing a prompt argument.
    """
    
    def __init__(self, name: str):
        """
        Initialize a PromptArgumentNode.
        
        Args:
            name: The name of the prompt argument node
        """
        super().__init__(name)
        self._required: bool = False
    
    def set_required(self, required: bool) -> None:
        """
        Set whether this argument is required.
        
        Args:
            required: True if required, False otherwise
        """
        self._required = required
    
    def is_required(self) -> bool:
        """
        Check if this argument is required.
        
        Returns:
            True if required, False otherwise
        """
        return self._required
    
    @property
    def required(self) -> bool:
        """Property access to required."""
        return self._required
    
    @required.setter
    def required(self, value: bool) -> None:
        """Property setter for required."""
        self._required = value
    
    def __str__(self) -> str:
        """
        Return string representation of the PromptArgumentNode.
        
        Returns:
            String representation including all fields
        """
        return (f"PromptArgumentNode [required={self._required}, name={self._name}, "
                f"title={self._title}, description={self._description}, meta={self._meta}]")
    
    def get_fully_qualified_name(self) -> str:
        """
        Get the fully qualified name of the node.
        
        Returns:
            The name of the node
        """
        return self._name
