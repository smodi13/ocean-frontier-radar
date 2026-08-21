"""Retrieval and classification behaviour."""
from ofr.lexicon import (CENTRALITY_VALUES, RELEVANCE_VALUES, classify,
                         load_lexicon, match_text, retrieve)

IOWA_STATE = ("Mitigating corrosion is a grand challenge costing the United States over "
              "half a trillion dollars annually. Current corrosion control relies on "
              "chemical coatings with high cost and health risks. Researchers will develop "
              "a biological microbial coating system for resilient corrosion protection.")
BIOMED = ("A multifunctional lipid nanoparticle delivery system for targeted delivery of "
          "vascular RNA therapeutics in patients with coronary blood vessel disease and "
          "tumor targeting in clinical trial settings.")
UNDERWATER = ("High-frequency Multiple-Input Multiple-Output MIMO underwater acoustic "
              "communication minimizes noise pollution in marine environments. Ocean "
              "technologies and the blue economy.")
GENERIC_AI = ("A predictive maintenance digital twin platform using computer vision "
              "inspection for industrial automation legacy systems.")


def test_lexicon_structure_is_complete():
    lex = load_lexicon()
    assert len(lex["categories"]) == 8
    for cid, cat in lex["categories"].items():
        assert cat["direct_terms"], cid
        assert "requires_ocean_context" in cat, cid
        assert cat["rationale"].strip(), cid


def test_hidden_adjacency_survives_without_ocean_vocabulary():
    """The Iowa State clause: no marine words, still retrieved."""
    c = classify(IOWA_STATE)
    assert "ocean" not in IOWA_STATE.lower() and "marine" not in IOWA_STATE.lower()
    assert c.relevance != "not_relevant"
    assert c.category_id == "marine_materials"
    assert c.ocean_centrality == "strong_adjacency"


def test_biomedical_text_is_rejected():
    assert classify(BIOMED).relevance == "not_relevant"


def test_underwater_comms_is_central_mechanism():
    c = classify(UNDERWATER)
    assert c.relevance == "relevant"
    assert c.ocean_centrality == "central_mechanism"


def test_generic_ai_without_marine_framing_is_incidental():
    c = classify(GENERIC_AI)
    assert c.relevance == "not_relevant"
    assert c.ocean_centrality == "incidental"


def test_retrieval_is_broader_than_classification():
    """Stage A must favour recall over Stage B precision."""
    borderline = "A new protective coating to reduce corrosion on structural steel."
    assert retrieve(borderline, min_score=3), "Stage A should retrieve this"


def test_classification_values_are_in_vocabulary():
    for text in (IOWA_STATE, BIOMED, UNDERWATER, GENERIC_AI):
        c = classify(text)
        assert c.relevance in RELEVANCE_VALUES
        assert c.ocean_centrality is None or c.ocean_centrality in CENTRALITY_VALUES


def test_empty_text_matches_nothing():
    assert match_text("") == []
    assert classify("").relevance == "not_relevant"


def test_rationale_is_always_populated():
    for text in (IOWA_STATE, BIOMED, UNDERWATER):
        assert classify(text).rationale.strip()


def test_plural_terms_match_singular_lexicon_entries():
    """Regression: 'Underwater Acoustic Communications' (plural) silently failed
    to match the lexicon term 'underwater acoustic communication', dropping a
    real Phase 1 top-five candidate from the Phase 2 universe."""
    text = ("High Data-Rate Multiple-Input Multiple-Output MIMO Underwater Acoustic "
            "Communications minimizing noise pollution in marine environments.")
    c = classify(text)
    assert c.relevance == "relevant"
    assert c.category_id == "ocean_sensing"


def test_single_direct_term_passes_stage_a():
    """A lone direct term scores 3; the Stage A gate must not exclude it."""
    assert retrieve("Unlimited marine energy for oceanic intelligence.", min_score=3)


def test_passing_mention_of_corrosion_is_not_marine_materials():
    """Regression: at a one-direct-term threshold, nuclear reactor components,
    industrial heat storage and building repainting were all admitted as marine
    materials on a single incidental 'corrosion'."""
    for text in [
        "Structural Components with Corrosion Resistant Surface Layers for Advanced "
        "Nuclear Reactor Systems. Advanced high temperature nuclear reactor systems.",
        "Painting Air Force buildings is manpower-intensive; corrosion control is needed.",
        "Integrated High Operating Temperature Heat Storage for Process Waste Heat with "
        "some corrosion concerns.",
    ]:
        assert classify(text).relevance == "not_relevant", text[:50]


def test_sustained_focus_on_corrosion_survives_without_ocean_words():
    """The Iowa State case: repeated, substantive treatment of the problem."""
    text = ("Mitigating corrosion is a grand challenge costing the United States over half "
            "a trillion dollars annually. Current corrosion control measures rely on "
            "chemical coatings. Microorganisms play key roles in corrosion, accelerating or "
            "inhibiting corrosion of metal surfaces. We develop a biological coating system "
            "for resilient corrosion protection.")
    c = classify(text)
    assert c.relevance != "not_relevant"
    assert c.ocean_centrality == "strong_adjacency"
