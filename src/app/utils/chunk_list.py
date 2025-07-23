from typing import List, Any

def chunk_list(list_to_chunk: List[Any], chunk_size: int) -> List[List[Any]]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")
    if not isinstance(list_to_chunk, list):
        raise TypeError("Input must be a list.")


    return [list_to_chunk[i:i + chunk_size] for i in range(0, len(list_to_chunk), chunk_size)]
