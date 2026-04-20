import re
import logging
from config import MAX_INPUT_LENGTH

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# INPUT SANITIZATION (PROMPT INJECTION PREVENTION)
# ─────────────────────────────────────────────────────────

def sanitize_input(user_input: str, max_length: int = None) -> str:
    """
    Sanitize user input to prevent prompt injection attacks.
    
    Args:
        user_input: Raw user input string
        max_length: Maximum allowed length (default from config)
    
    Returns:
        Sanitized input string
    """
    if max_length is None:
        max_length = MAX_INPUT_LENGTH
    
    if not user_input:
        return ""
    
    # Enforce length cap
    if len(user_input) > max_length:
        logger.warning(f"Input truncated from {len(user_input)} to {max_length} characters")
        user_input = user_input[:max_length]
    
    # Remove or escape potentially dangerous patterns
    # Remove newlines that could break prompt structure
    user_input = user_input.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    
    # Remove prompt injection markers (common attack patterns)
    dangerous_patterns = [
        r"ignore previous instructions",
        r"disregard prior prompt",
        r"forget.*instructions",
        r"system prompt",
        r"jailbreak",
    ]
    
    for pattern in dangerous_patterns:
        user_input = re.sub(pattern, "", user_input, flags=re.IGNORECASE)
    
    # Normalize whitespace (multiple spaces -> single space)
    user_input = " ".join(user_input.split())
    
    return user_input.strip()
