from mcp.shared.experimental.grouping.base_leaf_node import BaseLeafNode

class ToolNode(BaseLeafNode):
    """
    ToolNode class that extends BaseLeafNode functionality.
    Represents a tool node with input schema, output schema, and tool annotations.
    """

    def __init__(self, name):
        """
        Constructor for ToolNode.
        
        Args:
            name: The name of the tool node
        """
        # Call parent constructor (assuming BaseLeafNode is imported)
        super().__init__(name)
        
        # Protected fields (Python convention: single underscore prefix)
        self._input_schema = None
        self._output_schema = None
        self._tool_annotations = None

    def get_input_schema(self):
        """
        Get the input schema.
        
        Returns:
            The input schema string
        """
        return self._input_schema

    def set_input_schema(self, input_schema):
        """
        Set the input schema.
        
        Args:
            input_schema: The input schema string to set
        """
        self._input_schema = input_schema

    def get_output_schema(self):
        """
        Get the output schema.
        
        Returns:
            The output schema string
        """
        return self._output_schema

    def set_output_schema(self, output_schema):
        """
        Set the output schema.
        
        Args:
            output_schema: The output schema string to set
        """
        self._output_schema = output_schema

    def get_tool_annotations(self):
        """
        Get the tool annotations node.
        
        Returns:
            The ToolAnnotationsNode object
        """
        return self._tool_annotations

    def set_tool_annotations(self, tool_annotations):
        """
        Set the tool annotations node.
        
        Args:
            tool_annotations: The ToolAnnotationsNode object to set
        """
        self._tool_annotations = tool_annotations

    def __str__(self):
        """
        String representation of the ToolNode.
        
        Returns:
            A formatted string containing all relevant node information
        """
        return (f"ToolNode [name={self.name}, fqName={self.get_fully_qualified_name()}, "
                f"title={self.title}, description={self.description}, meta={self.meta}, "
                f"inputSchema={self._input_schema}, outputSchema={self._output_schema}, "
                f"toolAnnotation={self._tool_annotations}]")
