
import re

# Function 1: Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    return words


# Function 2: Naive String Matching
def naive_string_matching(text1, text2):
    matches = []

    for i in range(len(text1)):
        for j in range(len(text2)):
            if text1[i] == text2[j]:
                matches.append(text1[i])
                break

    return matches


# Function 3: Longest Common Subsequence
def lcs_similarity(text1, text2):
    m = len(text1)
    n = len(text2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_length = dp[m][n]

    if max(m, n) == 0:
        return 0

    similarity = (lcs_length / max(m, n)) * 100

    return round(similarity, 2)


# Function 4: Jaccard Similarity
def jaccard_similarity(text1, text2):
    set1 = set(text1)
    set2 = set(text2)

    if len(set1.union(set2)) == 0:
        return 0

    similarity = (len(set1.intersection(set2)) /
                  len(set1.union(set2))) * 100

    return round(similarity, 2)


# Function 5: Final Comparison
def compare_documents(text1, text2):

    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)

    common_words = naive_string_matching(words1, words2)

    lcs_score = lcs_similarity(words1, words2)

    jaccard_score = jaccard_similarity(words1, words2)

    return {
        "common_words": list(dict.fromkeys(common_words)),
        "lcs_similarity": lcs_score,
        "jaccard_similarity": jaccard_score
    }
