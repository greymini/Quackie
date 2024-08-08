import re

def normalize_code(code):
    """
    Normalize the code by converting multi-line strings to a single line,
    removing unnecessary newlines and extra spaces.

    Parameters:
    - code: Python code as a multi-line string

    Returns:
    - A single-line string with normalized formatting.
    """
    pattern = re.compile(r'\s*\n\s*')
    normalized_code = re.sub(pattern, ' ', code)
    
    normalized_code = re.sub(r'\s*\(\s*', '(', normalized_code)
    normalized_code = re.sub(r'\s*\)\s*', ')', normalized_code)
    
    return normalized_code

def resolve_diff(snippet_a, snippet_b):
    """
    Resolves the difference between two Python code snippets, ignoring comments.

    Parameters:
    - snippet_a: original Python code as a string
    - snippet_b: modified Python code as a string

    Returns:
    - A list of strings representing the differences.
    """
    def filter_non_comments(snippet):
        """
        Filters out comment lines from the code snippet.

        Parameters:
        - snippet: Python code as a string

        Returns:
        - A list of non-comment lines.
        """
        lines = snippet.splitlines()
        return [line for line in lines if not line.strip().startswith("#")]

    def extract_diffs(normalized_a, normalized_b):
        """
        Extracts the differences between two normalized code snippets.

        Parameters:
        - normalized_a: normalized original code as a list of strings
        - normalized_b: normalized modified code as a list of strings

        Returns:
        - A list of strings representing the differences.
        """
        diffs = []
        max_len = max(len(normalized_a), len(normalized_b))

        for i in range(max_len):
            if i >= len(normalized_a):
                diffs.append(f"+ {normalized_b[i]}")
            elif i >= len(normalized_b):
                diffs.append(f"- {normalized_a[i]}")
            else:
                if (normalized_a[i] != normalized_b[i]):
                    diffs.append(f"- {normalized_a[i]}")
                    diffs.append(f"+ {normalized_b[i]}")

        return diffs

    lines_a = filter_non_comments(snippet_a)
    lines_b = filter_non_comments(snippet_b)

    normalized_a = normalize_code('\n'.join(lines_a))
    normalized_b = normalize_code('\n'.join(lines_b))

    normalized_lines_a = normalized_a.split()
    normalized_lines_b = normalized_b.split()

    return extract_diffs(normalized_lines_a, normalized_lines_b)

def resolve_categorized_diff(snippet_a, snippet_b):
    """
    Resolves the categorized differences between two Python code snippets.

    Parameters:
    - snippet_a: original Python code as a string
    - snippet_b: modified Python code as a string

    Returns:
    - A list of dictionaries representing categorized differences.
    """
    def extract_comments(snippet):
        """
        Extracts comment lines from the code snippet.

        Parameters:
        - snippet: Python code as a string

        Returns:
        - A list of comment lines.
        """
        lines = snippet.splitlines()
        return [line for line in lines if line.strip().startswith("#")]

    def extract_diffs(lines_a, lines_b):
        """
        Extracts the differences between two code snippets.

        Parameters:
        - lines_a: list of lines from the original code
        - lines_b: list of lines from the modified code

        Returns:
        - A list of strings representing the differences.
        """
        diffs = []
        max_len = max(len(lines_a), len(lines_b))

        for i in range(max_len):
            if i >= len(lines_a):
                diffs.append(f"+ {lines_b[i]}")
            elif i >= len(lines_b):
                diffs.append(f"- {lines_a[i]}")
            else:
                if (lines_a[i] != lines_b[i]):
                    diffs.append(f"- {lines_a[i]}")
                    diffs.append(f"+ {lines_b[i]}")

        return diffs

    lines_a = snippet_a.splitlines()
    lines_b = snippet_b.splitlines()

    comments_a = extract_comments(snippet_a)
    comments_b = extract_comments(snippet_b)

    comment_diffs = extract_diffs(comments_a, comments_b)

    filtered_lines_a = [line for line in lines_a if not line.strip().startswith("#")]
    filtered_lines_b = [line for line in lines_b if not line.strip().startswith("#")]

    normalized_a = normalize_code('\n'.join(filtered_lines_a))
    normalized_b = normalize_code('\n'.join(filtered_lines_b))

    normalized_lines_a = normalized_a.split()
    normalized_lines_b = normalized_b.split()

    interpreter_diffs = extract_diffs(normalized_lines_a, normalized_lines_b)
    raw_diffs = extract_diffs(filtered_lines_a, filtered_lines_b)

    categorized_diffs = []

    # Extract interpreter diffs
    if interpreter_diffs:
        full_diff = f"- {' '.join(filtered_lines_a)}\n+ {' '.join(filtered_lines_b)}"
        categorized_diffs.append({"type": "interpreter", "diff": full_diff})

    # Extract formatting diffs
    formatting_diffs = [diff for diff in raw_diffs if diff not in interpreter_diffs and diff not in comment_diffs]
    if formatting_diffs:
        full_diff = '\n'.join(formatting_diffs)
        categorized_diffs.append({"type": "formatting", "diff": full_diff})

    # Extract comment diffs
    if comment_diffs:
        full_diff = '\n'.join(comment_diffs)
        categorized_diffs.append({"type": "comment", "diff": full_diff})

    return categorized_diffs

if __name__ == "__main__":
    snippet_a = (
        "# Router definition\n"
        "api_router = APIRouter()"
    )
    snippet_b = (
        "# Make sure endpoint are immune to missing trailing slashes\n"
        "api_router = APIRouter(redirect_slashes=True)"
    )
    snippet_c = (
        "# Router definition\n"
        "api_router = APIRouter(\n"
        "    redirect_slashes=True\n"
        ")"
    )

    print(resolve_diff(snippet_a, snippet_b))
    print(resolve_diff(snippet_b, snippet_c))
    print(resolve_categorized_diff(snippet_a, snippet_b))
    # print(resolve_categorized_diff(snippet_b, snippet_c))
