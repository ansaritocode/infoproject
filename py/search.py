import re

def clean_line(line):
    return line.strip().lower()

def parse_query(query):
    query = query.strip().lower()
    if " and " in query:
        keywords = query.split(" and ")
        return "AND", [k.strip() for k in keywords]
    elif " or " in query:
        keywords = query.split(" or ")
        return "OR", [k.strip() for k in keywords]
    elif " not " in query:
        keywords = query.split(" not ")
        return "NOT", [k.strip() for k in keywords]
    else:
        return "SINGLE", [query.strip()]

def search_text(text, query):
    lines = text.splitlines()
    mode, terms = parse_query(query)
    results = []

    for line in lines:
        clean = clean_line(line)
        if mode == "AND" and all(term in clean for term in terms):
            results.append(line)
        elif mode == "OR" and any(term in clean for term in terms):
            results.append(line)
        elif mode == "NOT" and terms[1] not in clean and terms[0] in clean:
            results.append(line)
        elif mode == "SINGLE" and terms[0] in clean:
            results.append(line)

    return "\n".join(results) or "No matches found."

def binary_search_text(text, keyword):
    lines = sorted([clean_line(l) for l in text.splitlines()])
    keyword = keyword.strip().lower()
    low, high = 0, len(lines) - 1

    while low <= high:
        mid = (low + high) // 2
        if lines[mid] == keyword:
            return f"Match found: {lines[mid]}"
        elif lines[mid] < keyword:
            low = mid + 1
        else:
            high = mid - 1

    return "No matches found with binary search."
