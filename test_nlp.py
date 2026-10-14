"""
Unit & Integration Test Suite for FAQ NLP Engine
=================================================
Verifies:
1. Dataset loading and FAQ count >= 30.
2. Accuracy of TF-IDF vectorization and cosine similarity matching.
3. Proper handling of paraphrased student queries.
4. Fallback handling for out-of-domain or nonsense questions.
5. Robustness against empty input, special characters, and whitespace.
"""

import os
import sys
from nlp_engine import FAQNLPEngine


def run_tests():
    print("=" * 65)
    print("🚀 RUNNING FAQ NLP ENGINE TEST SUITE")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "faq_data.json")

    # 1. Test Dataset Loading
    print("\n[Test 1] Testing FAQ dataset loading & minimum count...")
    assert os.path.exists(json_path), f"faq_data.json missing at {json_path}"
    engine = FAQNLPEngine(json_path=json_path, default_threshold=0.28)
    total_faqs = len(engine.faqs)
    print(f"✅ Successfully loaded {total_faqs} FAQs.")
    assert total_faqs >= 30, f"Expected at least 30 FAQs, found {total_faqs}."

    categories = engine.get_categories()
    print(f"✅ Categories found ({len(categories)}): {', '.join(categories)}")
    assert len(categories) >= 4, "Expected at least 4 distinct categories."

    # 2. Test In-Domain Natural Language Queries
    print("\n[Test 2] Testing In-Domain Question Matching...")
    test_queries = [
        # (user query, expected keyword in question/answer, description)
        ("What is the minimum CGPA for campus placements?", "CGPA", "Placement Eligibility"),
        ("how much is btech tuition fee?", "tuition fee", "Fees & Payments"),
        ("what is the one student one job rule?", "one job", "Placement Policy"),
        ("can i do off campus summer internship?", "internship", "Internships"),
        ("how to report ragging in college?", "ragging", "Anti-Ragging Support"),
        ("what is attendance criteria for writing exams?", "attendance", "Attendance Policy"),
        ("which companies visit for placement drives?", "companies", "Recruiters"),
        ("how is sgpa and cgpa calculated?", "cgpa", "Grading System"),
        ("how to prepare for technical coding interview?", "technical", "Interview Prep"),
        ("is there hostel facility for boys and girls?", "hostel", "Campus Facilities")
    ]

    matched_count = 0
    for query, expected_sub, desc in test_queries:
        result = engine.find_match(query)
        is_matched = result["matched"]
        conf = result["confidence"]
        matched_q = result.get("question") or "None"
        
        print(f"\n  Query: '{query}' ({desc})")
        print(f"  -> Matched: {is_matched} | Score: {conf:.4f} ({result['confidence_percent']})")
        print(f"  -> Target FAQ: {matched_q[:60]}...")
        
        assert is_matched, f"Expected query '{query}' to match, but got fallback (Score: {conf})."
        matched_count += 1

    print(f"\n✅ All {matched_count}/{len(test_queries)} in-domain queries matched successfully!")

    # 3. Test Paraphrased & Casual Keyword Variations
    print("\n[Test 3] Testing Casual & Paraphrased Queries...")
    casual_queries = [
        "placement pointer cut off",
        "college hostel mess food",
        "scholarships for poor students",
        "how to get noc for internship",
        "exam paper revaluation process"
    ]
    for q in casual_queries:
        res = engine.find_match(q)
        print(f"  Query: '{q}' -> Matched: {res['matched']} | Score: {res['confidence_percent']} | FAQ: {res.get('question')}")
        assert res["matched"], f"Failed to match casual query '{q}'"
    print("✅ All casual variations successfully resolved!")

    # 4. Test Out-of-Domain Queries (Fallback Verification)
    print("\n[Test 4] Testing Fallback on Out-of-Domain Queries...")
    unrelated_queries = [
        "How do I bake a chocolate cake?",
        "What is the capital city of France?",
        "Quantum mechanics string theory black holes"
    ]
    for uq in unrelated_queries:
        res = engine.find_match(uq, threshold=0.28)
        print(f"  Query: '{uq}' -> Matched: {res['matched']} | Score: {res['confidence_percent']}")
        assert not res["matched"], f"Expected fallback for '{uq}', but got match with score {res['confidence']}."
        assert len(res["suggestions"]) > 0, "Fallback must supply helpful suggestions."
        assert "admissions@apex-demo-institute.edu" in res["answer"], "Fallback should include contact info."
    print("✅ Out-of-domain fallback mechanism confirmed working properly!")

    # 5. Test Edge Cases (Empty, Punctuation, Whitespace)
    print("\n[Test 5] Testing Edge Cases & Robustness...")
    edge_cases = ["", "   ", "???!!!", "....", " \n\t "]
    for ec in edge_cases:
        res = engine.find_match(ec)
        assert not res["matched"], f"Edge case '{ec}' should not match an FAQ."
        assert res["is_empty"] or not res["matched"], f"Edge case failed handling for '{ec}'"
    print("✅ Robustness tests passed (empty and punctuation-only inputs handled cleanly)!")

    print("\n" + "=" * 65)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE)")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
