"""
category.py - Product Category Detection Utility
Uses simple keyword matching to identify the product category
mentioned in a review. No ML model required — pure Python logic.
"""

# ---------------------------------------------------------------------------
# CATEGORY KEYWORD MAP
# Each key is the category name; the list contains keywords to look for.
# The matching is case-insensitive.
# ---------------------------------------------------------------------------
CATEGORY_KEYWORDS = {
    "Phone":       ["phone", "smartphone", "mobile", "iphone", "android", "samsung", "pixel"],
    "Laptop":      ["laptop", "notebook", "macbook", "chromebook", "thinkpad"],
    "Chair":       ["chair", "seat", "stool", "recliner", "armchair", "sofa"],
    "Table":       ["table", "desk", "workstation", "countertop"],
    "Headphones":  ["headphones", "headphone", "earphones", "earbuds", "earpiece", "airpods"],
    "Keyboard":    ["keyboard", "keypad", "mechanical keyboard"],
    "Mouse":       ["mouse", "trackpad", "touchpad"],
    "TV":          ["tv", "television", "smart tv", "monitor", "screen", "display"],
    "Watch":       ["watch", "smartwatch", "wristwatch", "fitbit"],
    "Camera":      ["camera", "webcam", "dslr", "lens", "camcorder"],
}


def detect_category(review_text: str) -> str:
    """
    Detect the product category from a review using keyword matching.

    The function converts the review to lowercase and scans it for
    any keyword from the CATEGORY_KEYWORDS map.
    The first matching category is returned.
    If no match is found, "Other" is returned.

    Args:
        review_text (str): The raw review text entered by the user.

    Returns:
        str: The detected category name (e.g. "Laptop") or "Other".
    """

    # Convert to lowercase so matching is case-insensitive
    text_lower = review_text.lower()

    # Iterate over each category and its keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                # Found a matching keyword — return the category
                return category

    # No category detected
    return "Other"
