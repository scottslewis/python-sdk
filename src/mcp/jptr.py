"""JSON Pointer serialization support.  See serialize_jptr and deserialize_jptr below"""

from typing import Optional, Callable, Generator, Union, Iterable, Dict, List, Any
from urllib.parse import quote as encode_uri
from urllib.parse import unquote as decode_uri

# Type aliases to match the API
Json = Union[None, bool, int, float, str, list, dict]
JsonObject = dict
Getter = Callable[[Json], Optional[Json]]
Setter = Callable[[Json, Json], Json]
Assigner = Callable[[Json, Json], None]
Unsetter = Callable[[Json], Optional[Union[JsonObject, list]]]
Remover = Callable[[Json], None]

nil: str = ""

def pointerSegments(pointer: str) -> Generator[str, None, None]:
    """Generate segments from a JSON Pointer."""
    if len(pointer) > 0 and not pointer.startswith("/"):
        raise ValueError("Invalid JSON Pointer")
    
    segmentStart = 1
    segmentEnd = 0
    
    while segmentEnd < len(pointer):
        position = pointer.find("/", segmentStart)
        segmentEnd = len(pointer) if position == -1 else position
        segment = pointer[segmentStart:segmentEnd]
        segmentStart = segmentEnd + 1
        
        yield unescape(segment)


def get(pointer: str, subject: Optional[Json] = None) -> Union[Optional[Json], Getter]:
    """
    Get value at JSON Pointer location.
    
    Can be called with just pointer to return a getter function,
    or with both pointer and subject to return the value directly.
    """
    if subject is None:
        segments = list(pointerSegments(pointer))
        return lambda subject: _get(segments, subject)
    else:
        return _get(pointerSegments(pointer), subject)


def _get(segments: Iterable[str], subject: Optional[Json]) -> Optional[Json]:
    """Internal get implementation."""
    cursor: str = nil
    for segment in segments:
        subject = applySegment(subject, segment, cursor)
        cursor = append(segment, cursor)
    
    return subject


def set_p(pointer: str, subject: Optional[Json] = None, value: Optional[Json] = None) -> Union[Json, Setter]:
    """
    Set value at JSON Pointer location (immutable - returns new structure).
    
    Can be called with just pointer to return a setter function,
    or with pointer, subject, and value to return the modified structure directly.
    """
    if subject is None:
        return lambda subject, value: _set_p(pointerSegments(pointer), subject, value)
    else:
        return _set_p(pointerSegments(pointer), subject, value)


def _set_p(segments: Generator[str, None, None], subject: Optional[Json], value: Json, cursor: str = nil) -> Json:
    """Internal set implementation."""
    segment_result = next(segments, None)
    if segment_result is None:
        return value
    
    segment_value = segment_result
    
    if isinstance(subject, list):
        subject = subject.copy()
    elif isinstance(subject, dict):
        subject = subject.copy()
    else:
        applySegment(subject, segment_value, cursor)
    cursor = append(segment_value, cursor)
    
    # currentSubject could also be a list, but this appeases the type system
    currentSubject: Union[JsonObject, list] = subject
    computedSegment = computeSegment(subject, segment_value)
    currentSubject[computedSegment] = _set_p(segments, currentSubject[computedSegment] if computedSegment in currentSubject or (isinstance(currentSubject, list) and 0 <= computedSegment < len(currentSubject)) else None, value, cursor)
    return currentSubject


def assign(pointer: str, subject: Optional[Json] = None, value: Optional[Json] = None) -> Union[None, Assigner]:
    """
    Assign value at JSON Pointer location (mutable - modifies in place).
    
    Can be called with just pointer to return an assigner function,
    or with pointer, subject, and value to assign the value directly.
    """
    if subject is None:
        return lambda subject, value: _assign(pointerSegments(pointer), subject, value)
    else:
        return _assign(pointerSegments(pointer), subject, value)


def _assign(segments: Generator[str, None, None], subject: Json, value: Json, cursor: str = nil) -> None:
    """Internal assign implementation."""
    lastSegment: Optional[str] = None
    currentSubject: Optional[Json] = subject
    lastSubject: Optional[Json] = None
    
    for segment in segments:
        segment = computeSegment(currentSubject, segment)
        lastSegment = segment
        lastSubject = currentSubject
        currentSubject = applySegment(currentSubject, segment, cursor)
        cursor = append(str(segment), cursor)
    
    if lastSegment is None:
        return
    
    # lastSubject could also be a list, but this appeases the type system
    lastSubject[lastSegment] = value

def unset(pointer: str, subject: Optional[Json] = None) -> Union[Optional[Union[JsonObject, list]], Unsetter]:
    """
    Remove value at JSON Pointer location (immutable - returns new structure).
    
    Can be called with just pointer to return an unsetter function,
    or with pointer and subject to return the modified structure directly.
    """
    if subject is None:
        return lambda subject: _unset(pointerSegments(pointer), subject)
    else:
        return _unset(pointerSegments(pointer), subject)


def _unset(segments: Generator[str, None, None], subject: Optional[Json] = None, cursor: str = nil) -> Optional[Union[JsonObject, list]]:
    """Internal unset implementation."""
    segment_result = next(segments, None)
    if segment_result is None:
        return None
    
    segment_value = segment_result
    
    if isinstance(subject, list):
        subject = subject.copy()
    elif isinstance(subject, dict):
        subject = subject.copy()
    else:
        applySegment(subject, segment_value, cursor)
    cursor = append(segment_value, cursor)
    
    # currentSubject could also be a list, but this appeases the type system
    currentSubject: Union[JsonObject, list] = subject
    computedSegment = computeSegment(currentSubject, segment_value)
    unsetSubject = _unset(segments, currentSubject[computedSegment] if computedSegment in currentSubject or (isinstance(currentSubject, list) and 0 <= computedSegment < len(currentSubject)) else None, cursor)
    if computedSegment in currentSubject or (isinstance(currentSubject, list) and 0 <= computedSegment < len(currentSubject)):
        if unsetSubject is None:
            if isinstance(currentSubject, dict):
                del currentSubject[computedSegment]
            elif isinstance(currentSubject, list):
                del currentSubject[computedSegment]
        else:
            currentSubject[computedSegment] = unsetSubject
    return currentSubject


def remove(pointer: str, subject: Optional[Json] = None) -> Union[None, Remover]:
    """
    Remove value at JSON Pointer location (mutable - modifies in place).
    
    Can be called with just pointer to return a remover function,
    or with pointer and subject to remove the value directly.
    """
    if subject is None:
        return lambda subject: _remove(pointerSegments(pointer), subject)
    else:
        return _remove(pointerSegments(pointer), subject)


def _remove(segments: Generator[str, None, None], subject: Json, cursor: str = nil) -> None:
    """Internal remove implementation."""
    lastSegment: Optional[Union[str, int]] = None
    currentSubject: Optional[Json] = subject
    lastSubject: Optional[Json] = None
    
    for segment in segments:
        segment = computeSegment(currentSubject, segment)
        lastSegment = segment
        lastSubject = currentSubject
        currentSubject = applySegment(currentSubject, segment, cursor)
        cursor = append(str(segment), cursor)
    
    if lastSegment is None:
        return
    
    # lastSubject could also be a list, but this appeases the type system
    if isinstance(lastSubject, dict):
        del lastSubject[lastSegment]
    elif isinstance(lastSubject, list):
        del lastSubject[lastSegment]


def append(segment: Union[str, int], pointer: str) -> str:
    """Append a segment to a JSON Pointer."""
    return pointer + "/" + escape(str(segment))


def escape(segment: str) -> str:
    """Escape special characters in a JSON Pointer segment."""
    return str(segment).replace("~", "~0").replace("/", "~1")


def unescape(segment: str) -> str:
    """Unescape special characters in a JSON Pointer segment."""
    return str(segment).replace("~1", "/").replace("~0", "~")


def computeSegment(value: Optional[Json], segment: str) -> Union[str, int]:
    """
    Compute the actual segment to use based on the value type.
    
    For arrays, convert to integer or return length for "-".
    For objects, return the segment as-is.
    """
    if isinstance(value, list):
        return len(value) if segment == "-" else int(segment)
    else:
        return segment


def applySegment(value: Optional[Json], segment: Union[str, int], cursor: str = "") -> Optional[Json]:
    """Apply a segment to a value to retrieve the next value in the path."""
    if value is None:
        raise TypeError(f"Value at '{cursor}' is {'None' if cursor else 'undefined'} and does not have property '{segment}'")
    elif isScalar(value):
        value_type = type(value).__name__ if value is not None else "null"
        raise TypeError(f"Value at '{cursor}' is a {value_type} and does not have property '{segment}'")
    else:
        computedSegment = computeSegment(value, str(segment))
        if isinstance(value, dict):
            if computedSegment in value:
                return value[computedSegment]
        elif isinstance(value, list):
            if isinstance(computedSegment, int) and 0 <= computedSegment < len(value):
                return value[computedSegment]
        return None


def isScalar(value: Json) -> bool:
    """Check if a value is a scalar (not an object or array)."""
    return value is None or not isinstance(value, (dict, list))

# Type alias for JSON values
Json = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]

_REF_KEY = '$ref'

def _build_ptr(uri: str) -> Dict:
    return { _REF_KEY: '#' + encode_uri(uri)}

def serialize_jptr(subject: Json, 
              pointers: Optional[Dict[int, str]] = None, 
              location: str = "", 
              objectnamefield: str = "name",
              refbuilderfn: Callable[str, dict] = _build_ptr) -> Json:

    if pointers is None:
        pointers = {}
    # Handle boolean, float, bool, str
    if isinstance(subject, bool):
        return subject
    elif isinstance(subject, (int, float)) and not isinstance(subject, bool):
        return subject
    elif isinstance(subject, str):
        return subject
    # Handle None
    elif subject is None:
        return subject
    # Handle lists
    elif isinstance(subject, list):
        # Store location for this list
        pointers[id(subject)] = location
        # result is array
        result = []
        # Process array elements and append to result
        for index, value in enumerate(subject):
            if isinstance(value, (list, dict)) and id(value) in pointers:
                # If value is in pointers, then we call the refbuilderfn with the id of the value
                result.append(refbuilderfn(pointers[id(value)]))
            else:
                # otherwise we call ourselves recursively (depth first) and 
                # append to the location with the index
                result.append(serialize_jptr(value, pointers, append(str(index), location)))

        return result
    # Dictionaries
    elif isinstance(subject, dict):
        # store location for this obj_id (dict)
        pointers[id(subject)] = location
        # result is dictionary
        result = {}
        # Process dict key values
        for key, value in subject.items():
            if isinstance(value, (list, dict)) and id(value) in pointers:
                # If value is in pointers, then we create a json pointer to it
                result[key] = refbuilderfn(pointers[id(value)])
            else:
                # otherwise we call ourselves recursively (depth first) and 
                # append the key to the location
                result[key] = serialize_jptr(value, pointers, append(key, location))
        
        return result
    # Handle python objects
    elif isinstance(subject, object):
        # If it's an object
        try:
            # We first try to get it's name property if it has one
            obj_id = getattr(subject,objectnamefield)
        except Exception:
            # If it does not have a name then we get an object id
            obj_id = id(subject)
        # If the object id is already in pointers, then we return a json pointer
        if obj_id in pointers:
            return refbuilderfn(pointers[obj_id])
        else:
            pointers[obj_id] = location
            return serialize_jptr(subject.__dict__, pointers, location)
    else:
        # Fallback for any other type
        return subject

def deserialize_jptr(subject: Any, root = None, location: str = "") -> Any:
    if (isinstance(subject, (bool, int, float, str, type(None)))):
        return subject
    if not root:
        root = subject
    if isinstance(subject, list):
        for index, value in enumerate(subject):
            subject[index] = deserialize_jptr(value, root, append(str(index), location))
        return subject
    if isinstance(subject, dict):
        ref = subject.get(_REF_KEY, None)
        if isinstance(ref, str):
            fragment = ref.split('#', 2)[1]
            pointer = decode_uri(fragment)
            ref_value = get(pointer, root)
            if not ref_value:
                raise Exception("Invalid reference")
            return ref_value
    if isinstance(subject, object):
        obj_dict = subject if isinstance(subject, dict) else subject.__dict__
        for key, value in obj_dict.items():
            subject[key] = deserialize_jptr(value, root, append(key, location))
    return subject    

