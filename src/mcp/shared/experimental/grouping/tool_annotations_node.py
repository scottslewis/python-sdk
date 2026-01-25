from typing import Optional

class ToolAnnotationsNode:

    def __init__(self):
        # Protected fields
        self._title: Optional[str] = None
        self._read_only_hint: Optional[bool] = None
        self._destructive_hint: Optional[bool] = None
        self._idempotent_hint: Optional[bool] = None
        self._open_world_hint: Optional[bool] = None
        self._return_direct: Optional[bool] = None

    def get_title(self) -> Optional[str]:
        return self._title

    def set_title(self, title: Optional[str]) -> None:
        self._title = title

    def get_read_only_hint(self) -> Optional[bool]:
        return self._read_only_hint

    def set_read_only_hint(self, read_only_hint: Optional[bool]) -> None:
        self._read_only_hint = read_only_hint

    def get_destructive_hint(self) -> Optional[bool]:
        return self._destructive_hint

    def set_destructive_hint(self, destructive_hint: Optional[bool]) -> None:
        self._destructive_hint = destructive_hint

    def get_idempotent_hint(self) -> Optional[bool]:
        return self._idempotent_hint

    def set_idempotent_hint(self, idempotent_hint: Optional[bool]) -> None:
        self._idempotent_hint = idempotent_hint

    def get_open_world_hint(self) -> Optional[bool]:
        return self._open_world_hint

    def set_open_world_hint(self, open_world_hint: Optional[bool]) -> None:
        self._open_world_hint = open_world_hint

    def get_return_direct(self) -> Optional[bool]:
        return self._return_direct

    def set_return_direct(self, return_direct: Optional[bool]) -> None:
        self._return_direct = return_direct

    def __str__(self) -> str:
        return (f"ToolAnnotationNode [title={self._title}, readOnlyHint={self._read_only_hint}, "
                f"destructiveHint={self._destructive_hint}, idempotentHint={self._idempotent_hint}, "
                f"openWorldHint={self._open_world_hint}, returnDirect={self._return_direct}]")
