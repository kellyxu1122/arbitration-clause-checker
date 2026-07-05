"""
Sample arbitration clauses for testing and demonstration.
Includes both well-drafted ("healthy") clauses and clauses exhibiting
known pathologies, loosely modeled on patterns discussed in international
arbitration literature and reported jurisdictional-challenge cases.
"""

SAMPLE_CLAUSES = {
    "Healthy: standard ICC clause": (
        "Any dispute arising out of or in connection with this Agreement, "
        "including any question regarding its existence, validity or "
        "termination, shall be referred to and finally resolved by "
        "arbitration administered by the International Chamber of Commerce "
        "(ICC) in accordance with the ICC Rules of Arbitration. The seat of "
        "arbitration shall be Paris, France. The tribunal shall consist of "
        "three arbitrators. The language of the arbitration shall be "
        "English. This Agreement shall be governed by and construed in "
        "accordance with the laws of England and Wales."
    ),
    "Healthy: JAMS domestic (Comprehensive Rules, US seat)": (
        "Any controversy or claim arising out of or relating to this Agreement, "
        "or the breach thereof, shall be settled by arbitration administered by "
        "JAMS in accordance with its Comprehensive Arbitration Rules and "
        "Procedures. The seat of arbitration shall be San Francisco, California. "
        "The tribunal shall consist of one arbitrator. This Agreement is governed "
        "by California law."
    ),
    "Healthy: JAMS International (cross-border)": (
        "Any dispute arising out of or in connection with this contract shall be "
        "finally settled by arbitration administered by JAMS in accordance with "
        "the JAMS International Arbitration Rules. The seat of arbitration shall "
        "be New York, New York. The tribunal shall consist of three arbitrators. "
        "The language of the arbitration shall be English. This Agreement is "
        "governed by the laws of England and Wales."
    ),
    "Healthy: AAA/ICDR international": (
        "Any dispute arising out of or in connection with this contract shall be "
        "finally resolved by arbitration administered by the International Centre "
        "for Dispute Resolution (ICDR) in accordance with its International "
        "Arbitration Rules. The seat of arbitration shall be New York, New York. "
        "The tribunal shall consist of three arbitrators. The language of "
        "arbitration shall be English. This Agreement shall be governed by the "
        "laws of the State of New York."
    ),
    "Pathological: optional language ('may')": (
        "In the event of a dispute, either party may submit the matter to "
        "arbitration under the Rules of the International Chamber of "
        "Commerce."
    ),
    "Pathological: institution-rules mismatch": (
        "Any dispute shall be finally settled by arbitration administered "
        "by the Singapore International Arbitration Centre (SIAC) in "
        "accordance with the UNCITRAL Arbitration Rules. The seat of "
        "arbitration shall be Singapore."
    ),
    "Pathological: conflicting mechanisms": (
        "Any dispute arising under this Agreement may be referred to "
        "arbitration. Notwithstanding the foregoing, either party may also "
        "bring an action before a court of competent jurisdiction."
    ),
    "Pathological: garbled institution name": (
        "Any dispute shall be finally resolved by arbitration administered "
        "by the International Arbitration Commission of Singapore in "
        "accordance with its rules. The seat of arbitration shall be "
        "Singapore."
    ),
    "Pathological: missing seat and governing law": (
        "Any dispute arising out of or in connection with this Agreement "
        "shall be finally resolved by arbitration administered by the "
        "International Chamber of Commerce in accordance with the ICC "
        "Rules of Arbitration. The tribunal shall consist of one "
        "arbitrator."
    ),
    "Pathological: JAMS -- no rule set specified": (
        "Any dispute arising out of this Agreement shall be submitted to "
        "binding arbitration before JAMS. The seat shall be New York. "
        "The tribunal shall consist of one arbitrator. This Agreement is "
        "governed by New York law."
    ),
    "Pathological: JAMS Comprehensive Rules in international contract": (
        "Any international dispute arising out of this Agreement shall be "
        "finally resolved by arbitration administered by JAMS under its "
        "Comprehensive Arbitration Rules and Procedures. The seat shall be "
        "New York. This Agreement is governed by the laws of England and Wales."
    ),
    "Pathological: AAA Commercial Rules in international contract": (
        "Any international dispute arising under this Agreement shall be "
        "resolved by arbitration administered by the American Arbitration "
        "Association under its Commercial Arbitration Rules. The seat shall "
        "be New York. The laws of England and Wales govern this Agreement."
    ),
}
