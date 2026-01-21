import os
from typing import List
from .schemas import DocumentChunk

def load_knowledge_base(kb_dir: str) -> List[DocumentChunk]:
    chunks = []
    for filename in os.listdir(kb_dir):
        if not filename.endswith(".md"):
            continue
        
        filepath = os.path.join(kb_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_heading = "Overview"
        current_chunk_lines = []
        start_line = 1
        
        for i, line in enumerate(lines):
            line_num = i + 1
            if line.startswith("#"):
                # If we have content under the previous heading, save it
                if any(line.strip() for line in current_chunk_lines):
                    text = "".join(current_chunk_lines).strip()
                    if text:
                        chunks.append(DocumentChunk(
                            file=filename,
                            heading=current_heading,
                            text=text,
                            start_line=start_line,
                            end_line=line_num - 1,
                        ))

                # Start a new chunk
                current_heading = line.strip().lstrip("#").strip()
                current_chunk_lines = [line] # The heading line itself is part of the new chunk
                start_line = line_num
            else:
                current_chunk_lines.append(line)
        
        # Add the last chunk for the file
        if any(line.strip() for line in current_chunk_lines):
            text = "".join(current_chunk_lines).strip()
            if text:
                chunks.append(DocumentChunk(
                    file=filename,
                    heading=current_heading,
                    text=text,
                    start_line=start_line,
                    end_line=len(lines),
                ))
            
    return chunks
