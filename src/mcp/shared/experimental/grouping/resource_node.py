from typing import Optional
from mcp.shared.experimental.grouping.base_leaf_node import BaseLeafNode
from mcp.shared.experimental.grouping.annotations_node import AnnotationsNode

class ResourceNode(BaseLeafNode):
    
    def __init__(self, name: str):
        """
        Initialize a ResourceNode with the given name.
        
        Args:
            name: The name of the resource node
        """
        super().__init__(name)
        self._uri: Optional[str] = None
        self._size: Optional[int] = None
        self._mime_type: Optional[str] = None
        self._annotations: Optional['AnnotationsNode'] = None
    
    @property
    def uri(self) -> Optional[str]:
        return self._uri
    
    @uri.setter
    def uri(self, uri: str) -> None:
        self._uri = uri
    
    @property
    def size(self) -> Optional[int]:
        return self._size
    
    @size.setter
    def size(self, size: int) -> None:
        self._size = size
    
    @property
    def mimeType(self) -> Optional[str]:
        return self._mime_type
    
    @mimeType.setter
    def mimeType(self, mime_type: str) -> None:
        self._mime_type = mime_type
    
    @property
    def annotations(self) -> Optional[AnnotationsNode]:
        return self._annotations
    
    @annotations.setter
    def annotations(self, annotations: AnnotationsNode) -> None:
        self._annotations = annotations
    
    def __str__(self) -> str:
        return (f"ResourceNode [name={self.name}, fqName={self.get_fully_qualified_name()}, "
                f"title={self.title}, description={self.description}, meta={self.meta}, "
                f"uri={self._uri}, size={self._size}, mimeType={self._mime_type}, "
                f"annotations={self._annotations}]")
