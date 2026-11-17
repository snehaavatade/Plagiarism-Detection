
from plagiarism import compare_documents

# Original document
text1 = """
Machine learning is a branch of artificial intelligence.
It allows computers to learn from data.
"""

# Copied document
text2 = """
Machine learning is a branch of artificial intelligence.
It helps computers learn from data.
"""

# Compare both documents
result = compare_documents(text1, text2)

# Display results
print("PLAGIARISM DETECTION RESULTS")
print("----------------------------")

print("Common Words:", result["common_words"])

print("LCS Similarity:",
      result["lcs_similarity"], "%")

print("Jaccard Similarity:",
      result["jaccard_similarity"], "%")
