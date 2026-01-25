from typing import List, Optional
from mcp.shared.experimental.grouping.role_node import RoleNode

class AnnotationsNode:
    """
    AnnotationsNode class that holds audience, priority, and lastModified information.
    """

    def __init__(self, audience: Optional[List[RoleNode]], priority: Optional[float], last_modified: Optional[str]):
        """
        Initialize an AnnotationsNode instance.

        Args:
            audience: List of RoleNode objects representing the target audience
            priority: Priority value as a float
            last_modified: Last modification timestamp as a string
        """
        self._audience = audience
        self._priority = priority
        self._last_modified = last_modified

    def get_audience(self) -> Optional[List[RoleNode]]:
        """
        Get the audience list.

        Returns:
            List of RoleNode objects
        """
        return self._audience

    def set_audience(self, audience: Optional[List['RoleNode']]) -> None:
        """
        Set the audience list.

        Args:
            audience: List of RoleNode objects
        """
        self._audience = audience

    def get_priority(self) -> Optional[float]:
        """
        Get the priority value.

        Returns:
            Priority as a float
        """
        return self._priority

    def set_priority(self, priority: Optional[float]) -> None:
        """
        Set the priority value.

        Args:
            priority: Priority as a float
        """
        self._priority = priority

    def get_last_modified(self) -> Optional[str]:
        """
        Get the last modified timestamp.

        Returns:
            Last modified timestamp as a string
        """
        return self._last_modified

    def set_last_modified(self, last_modified: Optional[str]) -> None:
        """
        Set the last modified timestamp.

        Args:
            last_modified: Last modified timestamp as a string
        """
        self._last_modified = last_modified

    def __str__(self) -> str:
        """
        String representation of the AnnotationsNode.

        Returns:
            String representation in the format:
            "AnnotationsNode [audience=..., priority=..., lastModified=...]"
        """
        return f"AnnotationsNode [audience={self._audience}, priority={self._priority}, lastModified={self._last_modified}]"
