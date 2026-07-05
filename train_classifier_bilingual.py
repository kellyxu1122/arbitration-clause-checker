# -*- coding: utf-8 -*-
"""
Unified bilingual classifier for pathological arbitration clause detection.
================================================================================
Trains a SINGLE classifier that handles both English and Chinese clauses,
rather than two separate language-specific models. This is technically more
involved than a "detect language then route" approach because English and
Chinese require fundamentally different tokenization:

  - English: word-level tokenization works natively (whitespace-delimited).
  - Chinese: has no whitespace between words, so naive whitespace
    tokenization treats each *sentence* as one giant token, destroying all
    signal. We use jieba (a standard Chinese word segmentation library) to
    tokenize Chinese text into words first, then feed the result through
    the same TF-IDF + Logistic Regression pipeline used for English.

Both language's tokenized texts are combined into ONE vocabulary and ONE
feature space, so the resulting model can score a clause in either
language (or a code-switched mix of both, which does occur in real
bilingual contracts) without first deciding which language it's in.

Run with: python3 train_classifier_bilingual.py
"""

import re
import numpy as np
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
import joblib

from training_data_en import TRAINING_DATA as TRAINING_DATA_EN
from training_data_cn import TRAINING_DATA_CN


def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fa5]", text))


def tokenize_bilingual(text: str) -> str:
    """
    Normalize a clause (English, Chinese, or a code-switched mix) into a
    whitespace-joined token string suitable for TfidfVectorizer's default
    whitespace tokenizer.

    - If the text contains Chinese characters, segment Chinese spans with
      jieba while leaving embedded English words intact.
    - Pure English text passes through with standard lowercasing (jieba
      treats embedded ASCII words as their own tokens, so this also
      correctly handles mixed-language clauses).
    """
    if contains_chinese(text):
        tokens = jieba.lcut(text)
        # Filter out pure punctuation / whitespace tokens
        tokens = [t.strip() for t in tokens if t.strip() and not re.match(r"^[\s\W]+$", t)]
        return " ".join(tokens).lower()
    else:
        return text.lower()


def build_dataset():
    """Combine EN + CN datasets into one labeled set, tagging each example
    with its source language for reporting purposes (not used as a model
    feature -- the whole point is the model doesn't need to be told)."""
    examples = []
    for text, label in TRAINING_DATA_EN:
        examples.append((text, label, "en"))
    for text, label in TRAINING_DATA_CN:
        examples.append((text, label, "cn"))
    return examples


def main():
    examples = build_dataset()
    raw_texts = [e[0] for e in examples]
    labels = np.array([e[1] for e in examples])
    langs = np.array([e[2] for e in examples])

    print(f"Combined dataset: {len(examples)} clauses "
          f"({(langs == 'en').sum()} English, {(langs == 'cn').sum()} Chinese)")
    print(f"  Pathological: {labels.sum()}, Healthy: {len(labels) - labels.sum()}\n")

    tokenized = [tokenize_bilingual(t) for t in raw_texts]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True,
        token_pattern=r"(?u)\b\w+\b",
    )
    X = vectorizer.fit_transform(tokenized)

    clf = LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        C=1.0,
        random_state=42,
    )

    # Stratified k-fold (not leave-one-out) since the combined dataset is
    # large enough for a proper held-out fold structure (currently 303 clauses).
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = cross_val_predict(clf, X, labels, cv=skf)

    print("=" * 60)
    print("5-fold cross-validation results (combined EN+CN)")
    print("=" * 60)
    print(classification_report(labels, y_pred, target_names=["healthy", "pathological"]))
    print("Confusion matrix:")
    print(confusion_matrix(labels, y_pred))

    # Per-language breakdown -- this is the key question for a bilingual
    # model: does accuracy hold separately within each language, or is
    # the headline number propped up by one language being easier?
    print()
    print("=" * 60)
    print("Per-language accuracy breakdown")
    print("=" * 60)
    for lang in ["en", "cn"]:
        mask = langs == lang
        acc = (y_pred[mask] == labels[mask]).mean()
        print(f"  {lang.upper()}: {acc:.1%} accuracy ({mask.sum()} examples)")

    # Fit final model on all data
    clf.fit(X, labels)
    joblib.dump(
        {"vectorizer": vectorizer, "classifier": clf, "tokenizer": "jieba_bilingual"},
        "clause_classifier_bilingual.joblib",
    )
    print("\nSaved bilingual model to clause_classifier_bilingual.joblib")

    # Inspect top features by language script to sanity-check the model
    # is actually using signal from both languages, not just one.
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = clf.coef_[0]

    def is_chinese_token(tok):
        return bool(re.search(r"[\u4e00-\u9fa5]", tok))

    cn_mask = np.array([is_chinese_token(f) for f in feature_names])
    en_mask = ~cn_mask

    print()
    print("=" * 60)
    print("Top 10 Chinese-token features -> pathological")
    print("=" * 60)
    cn_coefs = coefs.copy()
    cn_coefs[~cn_mask] = -np.inf
    for idx in np.argsort(cn_coefs)[-10:][::-1]:
        if coefs[idx] > 0:
            print(f"  {feature_names[idx]:20s}  weight={coefs[idx]:.3f}")

    print()
    print("=" * 60)
    print("Top 10 English-token features -> pathological")
    print("=" * 60)
    en_coefs = coefs.copy()
    en_coefs[~en_mask] = -np.inf
    for idx in np.argsort(en_coefs)[-10:][::-1]:
        if coefs[idx] > 0:
            print(f"  {feature_names[idx]:20s}  weight={coefs[idx]:.3f}")


if __name__ == "__main__":
    main()
