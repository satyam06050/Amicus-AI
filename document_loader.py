# ─────────────────────────────────────────────────────────
# DOCUMENT LOADER & PROCESSOR
# ─────────────────────────────────────────────────────────

import logging
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# PDF & TEXT EXTRACTION
# ─────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file using PyPDF2 with memory efficiency."""
    try:
        import PyPDF2
    except ImportError:
        logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
        return ""
    
    try:
        text = ""
        max_pages = None  # Set to a number to limit pages for very large PDFs
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            logger.info(f"[PDF] Total pages in {Path(pdf_path).name}: {total_pages}")
            
            # Limit to first 30 pages for very large PDFs to avoid memory issues and speed up processing
            if total_pages > 30:
                logger.warning(f"[PDF] PDF has {total_pages} pages, limiting to first 30 for faster processing")
                max_pages = 30
            
            for page_num, page in enumerate(pdf_reader.pages[:max_pages], 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    # Log progress every 10 pages
                    if page_num % 10 == 0:
                        logger.debug(f"[PDF] Processed {page_num} pages, text size: {len(text)} chars")
                except Exception as e:
                    logger.warning(f"[PDF] Error extracting page {page_num}: {str(e)}")
                    continue
        
        logger.info(f"[PDF] Completed: extracted {len(text)} characters from {Path(pdf_path).name}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        return ""

def extract_text_from_txt(txt_path: str) -> str:
    """Extract text from plain text file."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        logger.error(f"Error reading text file {txt_path}: {str(e)}")
        return ""

def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        from docx import Document
    except ImportError:
        logger.error("python-docx not installed. Install with: pip install python-docx")
        return ""
    
    try:
        doc = Document(docx_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {docx_path}: {str(e)}")
        return ""

def load_document(file_path: str) -> Tuple[str, str]:
    """
    Load document from file.
    
    Args:
        file_path: Path to document file
    
    Returns:
        Tuple of (text, file_type)
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if suffix == ".pdf":
        text = extract_text_from_pdf(file_path)
        return text, "pdf"
    elif suffix == ".txt":
        text = extract_text_from_txt(file_path)
        return text, "txt"
    elif suffix == ".docx":
        text = extract_text_from_docx(file_path)
        return text, "docx"
    else:
        logger.error(f"Unsupported file type: {suffix}")
        return "", ""

# ─────────────────────────────────────────────────────────
# TEXT CHUNKING
# ─────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    """
    Split text into overlapping chunks in a memory-efficient way.
    Optimized for faster embedding with larger chunks.
    
    Args:
        text: Input text
        chunk_size: Size of each chunk in characters (default 1000 for faster processing)
        overlap: Overlap between chunks in characters (default 150)
    
    Returns:
        List of text chunks
    """
    if not text or len(text) < chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    
    try:
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
            start = end - overlap
            
            # ChromaDB max batch size is ~5461, limit to 2000 to speed up processing
            if len(chunks) > 2000:
                logger.warning(f"[CHUNK] Too many chunks created ({len(chunks)}), stopping at 2000 to speed up processing")
                break
    except MemoryError as e:
        logger.error(f"[CHUNK] MemoryError during chunking: {str(e)}")
        # Return what we have so far
        if not chunks:
            # If we couldn't create even one chunk, split the text into smaller pieces
            logger.info(f"[CHUNK] Splitting large text ({len(text)} chars) into smaller pieces")
            half = len(text) // 2
            return [text[:half], text[half:]]
    
    return chunks

# ─────────────────────────────────────────────────────────
# CHROMADB INTEGRATION
# ─────────────────────────────────────────────────────────

def add_documents_to_collection(
    collection,
    embedder,
    file_paths: List[str],
    doc_source: str = "uploaded"
) -> Dict[str, int]:
    """
    Add documents from files to ChromaDB collection.
    
    Args:
        collection: ChromaDB collection
        embedder: Sentence transformer embedder
        file_paths: List of file paths
        doc_source: Source label (e.g., "uploaded", "knowledge_base")
    
    Returns:
        Dictionary with statistics
    """
    stats = {
        "files_processed": 0,
        "chunks_added": 0,
        "chunks_failed": 0,
        "errors": []
    }
    
    BATCH_SIZE = 64  # Embed in larger batches for faster processing (still safe for memory)
    COLLECTION_BATCH_SIZE = 4000  # ChromaDB max is ~5461, use 4000 to be safe
    
    for file_idx, file_path in enumerate(file_paths, 1):
        try:
            logger.info(f"[KB_ADD] [{file_idx}/{len(file_paths)}] Loading document: {file_path}")
            text, file_type = load_document(file_path)
            if not text:
                msg = f"No text extracted from {file_path}"
                logger.warning(f"[KB_ADD] {msg}")
                stats["errors"].append(msg)
                continue
            
            logger.info(f"[KB_ADD] Extracted {len(text)} characters from {file_path}")
            
            # Chunk the text
            chunks = chunk_text(text)
            file_name = Path(file_path).name
            logger.info(f"[KB_ADD] Created {len(chunks)} chunks from {file_name}")
            
            # Create IDs based on file name and chunk index
            file_hash = hashlib.md5(file_name.encode()).hexdigest()[:8]
            
            # Process chunks in batches to avoid memory issues
            try:
                logger.info(f"[KB_ADD] Starting batch embedding of {len(chunks)} chunks from {file_name}...")
                
                all_chunk_ids = []
                all_documents = []
                all_metadatas = []
                all_embeddings = []
                
                # Process chunks in embedding batches
                for batch_start in range(0, len(chunks), BATCH_SIZE):
                    batch_end = min(batch_start + BATCH_SIZE, len(chunks))
                    batch_chunks = chunks[batch_start:batch_end]
                    
                    logger.debug(f"[KB_ADD] Embedding batch {batch_start}-{batch_end} of {len(chunks)}")
                    
                    try:
                        # Embed this batch
                        batch_embeddings = embedder.encode(batch_chunks).tolist()
                        
                        # Add to lists for collection insert
                        for chunk_idx, chunk in enumerate(batch_chunks, batch_start):
                            chunk_id = f"chunk_{doc_source}_{file_hash}_{chunk_idx}"
                            all_chunk_ids.append(chunk_id)
                            all_documents.append(chunk)
                            all_metadatas.append({
                                "source": doc_source,
                                "file_name": file_name,
                                "file_type": file_type,
                                "chunk_index": chunk_idx,
                                "topic": f"{file_name} (Part {chunk_idx + 1})"
                            })
                            all_embeddings.append(batch_embeddings[chunk_idx - batch_start])
                    except Exception as batch_err:
                        logger.error(f"[KB_ADD] Error in batch {batch_start}-{batch_end}: {str(batch_err)}", exc_info=True)
                        stats["chunks_failed"] += len(batch_chunks)
                        stats["errors"].append(f"Batch {batch_start}-{batch_end}: {str(batch_err)[:100]}")
                
                # Now insert into collection in smaller batches to respect ChromaDB limits
                if all_chunk_ids:
                    logger.info(f"[KB_ADD] Adding {len(all_chunk_ids)} chunks to collection in batches of {COLLECTION_BATCH_SIZE}...")
                    
                    for coll_batch_start in range(0, len(all_chunk_ids), COLLECTION_BATCH_SIZE):
                        coll_batch_end = min(coll_batch_start + COLLECTION_BATCH_SIZE, len(all_chunk_ids))
                        
                        logger.debug(f"[KB_ADD] Inserting collection batch {coll_batch_start}-{coll_batch_end}")
                        
                        try:
                            collection.add(
                                ids=all_chunk_ids[coll_batch_start:coll_batch_end],
                                documents=all_documents[coll_batch_start:coll_batch_end],
                                embeddings=all_embeddings[coll_batch_start:coll_batch_end],
                                metadatas=all_metadatas[coll_batch_start:coll_batch_end]
                            )
                        except Exception as coll_err:
                            logger.error(f"[KB_ADD] Error inserting collection batch {coll_batch_start}-{coll_batch_end}: {str(coll_err)}", exc_info=True)
                            stats["errors"].append(f"Collection batch {coll_batch_start}-{coll_batch_end}: {str(coll_err)[:100]}")
                            stats["chunks_failed"] += (coll_batch_end - coll_batch_start)
                            continue
                    
                    stats["chunks_added"] += len(all_chunk_ids)
                    logger.info(f"[KB_ADD] ✓ Successfully added {len(all_chunk_ids)} chunks from {file_name}")
                
            except Exception as e:
                msg = f"Failed to embed and add chunks from {file_path}: {str(e)}"
                logger.error(f"[KB_ADD] {msg}", exc_info=True)
                stats["errors"].append(msg)
                stats["chunks_failed"] += len(chunks)
            
            stats["files_processed"] += 1
            
        except Exception as e:
            msg = f"Error processing {file_path}: {str(e)}"
            logger.error(f"[KB_ADD] {msg}", exc_info=True)
            stats["errors"].append(msg)
    
    return stats

def get_uploaded_documents(uploads_dir: str) -> List[str]:
    """Get list of uploaded document files."""
    uploads_path = Path(uploads_dir)
    if not uploads_path.exists():
        return []
    
    supported_extensions = {".pdf", ".txt", ".docx"}
    files = []
    
    for file_path in uploads_path.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            files.append(str(file_path))
    
    return sorted(files)
