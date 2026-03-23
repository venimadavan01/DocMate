import os


# --------------------------------------------------
# FILE VALIDATION
# --------------------------------------------------
# Validates whether the given file exists and is supported
# Supports both direct path and files inside "data/" directory
def validate_file(file_path):

    # Check if file exists in given path
    if os.path.exists(file_path):
        final_path = file_path

    # Check if file exists inside "data" folder
    elif os.path.exists(os.path.join("data", file_path)):
        final_path = os.path.join("data", file_path)

    # File not found
    else:
        raise FileNotFoundError("File does not exist")

    # Validate supported formats
    if not (final_path.endswith(".pdf") or final_path.endswith(".txt")):
        raise ValueError("Only PDF and TXT files are supported")

    return final_path


# --------------------------------------------------
# SOURCE FORMATTING
# --------------------------------------------------
# Formats retrieved documents for UI display
# Extracts page number (if available) and source metadata
def format_sources(docs, max_sources=2):
    formatted = []

    # Limit number of sources shown
    for i, doc in enumerate(docs[:max_sources]):

        # Clean content (not currently used, but kept for flexibility)
        content = doc.page_content.strip().replace("\n", " ")

        # Extract page number from metadata
        preview = doc.metadata.get("page", "N/A")

        # Convert page number to human-readable format (0 → 1)
        if preview != "N/A":
            try:
                preview = int(preview) + 1
            except ValueError:
                # Handle invalid page formats
                preview = "N/A"

        # Extract source file name
        source = doc.metadata.get("source", "Unknown")

        # Structured output for frontend
        formatted.append({
            "id": i,
            "source": source,
            "text": "Page Number: " + str(preview)
        })

    return formatted


# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------
# Removes leading/trailing whitespace from text
def clean_text(text):
    return text.strip()


# --------------------------------------------------
# DEBUG HELPER
# --------------------------------------------------
# Prints a visual separator in console logs
# Useful for debugging and readability
def print_separator():
    print("\n" + "=" * 50 + "\n")