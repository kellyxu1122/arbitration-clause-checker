"""
Pathological Arbitration Clause Detector
==========================================
A rule-based engine that scans an English arbitration clause and flags
common drafting defects known in international arbitration practice as
"pathological clauses" -- defects that can render a clause unenforceable
or trigger jurisdictional challenges.

Reference categories (based on established international arbitration
literature, e.g. ICC guidance, Redfern & Hunter on International
Arbitration):
  1. Institution name / reference errors
  2. Rules-institution mismatch
  3. Optional / non-mandatory language ("may" vs "shall")
  4. Multi-tier / conflicting dispute resolution mechanisms
  5. Missing or contradictory seat of arbitration
  6. Vague or missing governing law
  7. Ambiguous scope of arbitrable disputes
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Flag:
    category: str
    severity: str          # "high" | "medium" | "low"
    message: str
    matched_text: str = ""
    start: int = -1
    end: int = -1


@dataclass
class AnalysisResult:
    clause: str
    flags: List[Flag] = field(default_factory=list)

    @property
    def risk_score(self) -> int:
        """Simple weighted score: high=3, medium=2, low=1."""
        weights = {"high": 3, "medium": 2, "low": 1}
        return sum(weights[f.severity] for f in self.flags)

    @property
    def risk_level(self) -> str:
        score = self.risk_score
        if score == 0:
            return "Low risk"
        elif score <= 3:
            return "Moderate risk"
        else:
            return "High risk"


# ---------------------------------------------------------------------------
# Known institution names and their commonly associated rule sets.
# Used to detect Category 2 (rules-institution mismatch).
# ---------------------------------------------------------------------------
INSTITUTION_RULES_MAP = {
    "icc": ["icc rules", "rules of arbitration of the international chamber of commerce"],
    "lcia": ["lcia rules", "lcia arbitration rules"],
    "siac": ["siac rules"],
    "hkiac": ["hkiac rules", "hkiac administered arbitration rules"],
    "cietac": ["cietac rules", "cietac arbitration rules"],
    "scc": ["scc rules", "arbitration rules of the scc"],
    "icsid": ["icsid rules", "icsid convention"],
    # AAA has two distinct rule sets: Commercial Arbitration Rules (domestic) and
    # International Arbitration Rules (international/cross-border). Specifying
    # the wrong set is a common drafting error in cross-border contracts.
    "american arbitration association": [
        "commercial arbitration rules", "international arbitration rules",
        "aaa commercial", "aaa international",
    ],
    "aaa": [
        "commercial arbitration rules", "international arbitration rules",
        "aaa commercial", "aaa international",
    ],
    # AFA has its own Rules of Arbitration (Règlement d'arbitrage de l'AFA).
    # A clause naming AFA but citing ICC or UNCITRAL Rules is a mismatch.
    "afa": ["afa rules", "afa arbitration rules", "règlement d'arbitrage de l'afa"],
    "association française d'arbitrage": [
        "afa rules", "afa arbitration rules", "règlement d'arbitrage de l'afa",
    ],
    # $250k+ threshold default) and International Arbitration Rules. For
    # cross-border disputes, JAMS International Rules should be specified
    # explicitly; relying on the default Comprehensive Rules in an international
    # context is a recognised drafting risk.
    "jams": [
        "jams comprehensive", "jams international", "jams arbitration rules",
        "jams rules", "comprehensive arbitration rules and procedures",
        "jams international arbitration rules",
    ],
}

# Common known institutions, used to detect garbled / non-existent names.
KNOWN_INSTITUTIONS = [
    "international chamber of commerce", "icc",
    "london court of international arbitration", "lcia",
    "singapore international arbitration centre", "siac",
    "hong kong international arbitration centre", "hkiac",
    "china international economic and trade arbitration commission", "cietac",
    "stockholm chamber of commerce", "scc",
    "international centre for settlement of investment disputes", "icsid",
    "american arbitration association", "aaa",
    "international centre for dispute resolution", "icdr",
    "jams", "jams international",
    "uncitral",
    # AFA -- Association Française d'Arbitrage (France's primary domestic
    # arbitration institution; Paris is a leading international seat)
    "association française d'arbitrage", "afa",
    "association francaise d'arbitrage",
    # additional institutions represented in the extended dataset
    "german arbitration institute", "dis",
    "japan commercial arbitration association", "jcaa",
    "korean commercial arbitration board", "kcab",
    "dubai international arbitration centre", "diac",
    "vienna international arbitral centre", "viac",
    "australian centre for international commercial arbitration", "acica",
    "milan chamber of arbitration",
    "cairo regional centre for international commercial arbitration", "crcica",
    "beijing arbitration commission", "bac",
    "shanghai international arbitration centre", "shiac",
    "permanent court of arbitration", "pca",
]


def _find_all(pattern, text, flags=re.IGNORECASE):
    return list(re.finditer(pattern, text, flags))


def check_optional_language(text: str) -> List[Flag]:
    """Category 3: 'may' instead of 'shall' creates ambiguity about whether
    arbitration is mandatory or merely an option."""
    flags = []
    for m in _find_all(r"\b(may|might|could)\s+(submit|refer|elect to refer|choose to submit)\b", text):
        flags.append(Flag(
            category="Consent & Jurisdiction Conflict — ambiguous 'may' instead of 'shall'",
            severity="high",
            message=(
                "Use of '%s' instead of 'shall'/'will' creates ambiguity about "
                "whether arbitration is mandatory. Courts in several jurisdictions "
                "have held such clauses to be a mere option to arbitrate rather than "
                "a binding agreement, undermining enforceability." % m.group(1)
            ),
            matched_text=m.group(0),
            start=m.start(), end=m.end(),
        ))
    return flags


def check_multi_tier_conflict(text: str) -> List[Flag]:
    """Category 4: clause references both arbitration and litigation/courts
    without a clear, exclusive hierarchy."""
    flags = []
    has_arbitration = re.search(r"\barbitrat", text, re.IGNORECASE)
    has_litigation = re.search(r"\b(litigation|court of competent jurisdiction|sue|lawsuit|civil action)\b", text, re.IGNORECASE)
    has_exclusivity = re.search(r"\b(exclusively|solely|finally|exclusive jurisdiction)\b", text, re.IGNORECASE)
    if has_arbitration and has_litigation and not has_exclusivity:
        m = has_litigation
        flags.append(Flag(
            category="Consent & Jurisdiction Conflict — arbitration and litigation both permitted",
            severity="high",
            message=(
                "The clause references both arbitration and court litigation without "
                "clearly establishing which mechanism is exclusive or which takes "
                "precedence. This is a classic 'multi-tier' pathology that can lead to "
                "parallel proceedings or a party arguing arbitration was never "
                "mandatory."
            ),
            matched_text=m.group(0),
            start=m.start(), end=m.end(),
        ))
    return flags


def check_institution_rules_mismatch(text: str) -> List[Flag]:
    """Category 2: named institution does not match the named rules
    (e.g., 'administered by SIAC' but 'under the UNCITRAL Arbitration Rules'
    without clarifying SIAC will administer under those rules)."""
    flags = []
    lower = text.lower()
    mentioned_uncitral = "uncitral" in lower

    for inst, valid_rule_phrases in INSTITUTION_RULES_MAP.items():
        inst_pattern = r"\b" + re.escape(inst) + r"\b"
        inst_match = re.search(inst_pattern, lower)
        if not inst_match:
            continue
        rules_match = any(phrase in lower for phrase in valid_rule_phrases)
        if mentioned_uncitral and not rules_match:
            flags.append(Flag(
                category="Institutional Designation — named institution and cited rules conflict",
                severity="high",
                message=(
                    "The clause names '%s' as the administering institution but "
                    "refers to the UNCITRAL Arbitration Rules without clarifying "
                    "that %s will administer the arbitration under those rules "
                    "(ad hoc vs. institutional administration is unclear). "
                    "Institutions and rule sets should be explicitly paired, e.g. "
                    "'... administered by %s in accordance with the UNCITRAL "
                    "Arbitration Rules.'" % (inst.upper(), inst.upper(), inst.upper())
                ),
                matched_text=inst_match.group(0),
            ))
    return flags


def check_garbled_institution_name(text: str) -> List[Flag]:
    """Category 1: references an arbitration institution but the name does
    not match any commonly recognized institution -- may indicate a typo
    or a non-existent body."""
    flags = []
    # Look for patterns like "X Arbitration Commission/Centre/Court/Association"
    candidates = _find_all(
        r"\b(?:administered by|under the auspices of)\s+(the\s+)?"
        r"((?:[A-Z][a-zA-Z&]*\s+){1,5}Arbitration\s+(?:Commission|Centre|Center|Court|Association|Institute|Chamber))",
        text,
    )
    lower = text.lower()
    for m in candidates:
        name = m.group(2).strip().lower()
        recognized = any(known in name or name in known for known in KNOWN_INSTITUTIONS)
        if not recognized:
            flags.append(Flag(
                category="Institutional Designation — unrecognized institution name",
                severity="medium",
                message=(
                    "The referenced institution '%s' does not match any widely "
                    "recognized arbitration institution. Verify the exact legal name "
                    "and registered seat of the institution -- misnamed or "
                    "non-existent institutions are a leading cause of pathological "
                    "clauses and can render the arbitration agreement inoperable."
                    % m.group(2).strip()
                ),
                matched_text=m.group(2).strip(),
                start=m.start(2), end=m.end(2),
            ))
    return flags


def check_missing_seat(text: str) -> List[Flag]:
    """Category 5: no seat/place of arbitration specified."""
    flags = []
    has_arbitration = re.search(r"\barbitrat", text, re.IGNORECASE)
    has_seat = re.search(
        r"\b(seat of (the )?arbitration|place of arbitration|arbitration shall (be )?(held|take place|be seated) in|seated in|the seat shall be)\b",
        text, re.IGNORECASE,
    )
    if has_arbitration and not has_seat:
        flags.append(Flag(
            category="Missing Procedural Elements — no seat of arbitration specified",
            severity="high",
            message=(
                "No seat (legal place) of arbitration is specified. The seat "
                "determines the procedural (lex arbitri) law governing the "
                "arbitration and which national courts have supervisory "
                "jurisdiction. Absent an express seat, this must be determined by "
                "the institution or tribunal by default, adding cost, delay and "
                "uncertainty."
            ),
        ))
    return flags


def check_missing_governing_law(text: str) -> List[Flag]:
    """Category 6: no governing law of the contract specified."""
    flags = []
    has_law = re.search(
        r"\b(governed by|governing law|laws of|construed in accordance with)\b",
        text, re.IGNORECASE,
    )
    if not has_law:
        flags.append(Flag(
            category="Missing Procedural Elements — governing law not specified",
            severity="medium",
            message=(
                "No governing law of the underlying contract is specified. While "
                "this is sometimes addressed elsewhere in the contract, its absence "
                "from the dispute resolution clause is a common oversight that can "
                "create disputes about which substantive law applies, separate from "
                "the law governing the arbitration agreement itself."
            ),
        ))
    return flags


def check_vague_scope(text: str) -> List[Flag]:
    """Category 7: scope of arbitrable disputes is vague or unreasonably narrow."""
    flags = []
    broad_scope = re.search(
        r"\b(any dispute|all disputes|any controversy|any claim).{0,40}(arising (out of|from)|in connection with|relating to)",
        text, re.IGNORECASE,
    )
    if not broad_scope:
        flags.append(Flag(
            category="Missing Procedural Elements — vague or narrow scope of disputes",
            severity="low",
            message=(
                "The clause does not use a standard broad-scope formulation (e.g. "
                "'any dispute arising out of or in connection with this Agreement'). "
                "Narrowly or vaguely drafted scope language can allow a party to "
                "argue that a particular claim falls outside the arbitration "
                "agreement, fragmenting proceedings between arbitration and "
                "litigation."
            ),
        ))
    return flags


def check_number_of_arbitrators(text: str) -> List[Flag]:
    """Bonus check: missing specification of tribunal size, a common
    source of delay/dispute at the outset of proceedings."""
    flags = []
    has_arbitration = re.search(r"\barbitrat", text, re.IGNORECASE)
    has_number = re.search(r"\b(one|two|three|sole|single|panel of \d+|\d+\s+arbitrators?)\b", text, re.IGNORECASE)
    if has_arbitration and not has_number:
        flags.append(Flag(
            category="Missing Procedural Elements — number of arbitrators not specified",
            severity="low",
            message=(
                "The clause does not specify the number of arbitrators. Most "
                "institutional rules provide a default (often one, sometimes "
                "three), but leaving this unspecified can still generate "
                "disagreement between the parties at the outset of a dispute."
            ),
        ))
    return flags


def check_jams_international_rule_set(text: str) -> List[Flag]:
    """JAMS-specific check: JAMS operates two distinct rule sets:
      - JAMS Comprehensive Arbitration Rules & Procedures (domestic US default,
        applies by default to claims over $250,000 when no rules are specified)
      - JAMS International Arbitration Rules (designed for cross-border disputes)
    A clause that names JAMS without specifying which rule set applies -- or that
    is in an international contract but specifies the Comprehensive Rules without
    noting their domestic default scope -- creates ambiguity about procedure,
    discovery scope, and arbitrator appointment. This check flags such clauses
    as a medium-severity concern warranting explicit rule-set specification."""
    flags = []
    lower = text.lower()
    has_jams = "jams" in lower
    if not has_jams:
        return flags
    # Check if the clause specifies any rule set at all
    has_explicit_rules = re.search(
        r"\b(jams\s+comprehensive|jams\s+international|comprehensive\s+arbitration\s+rules|"
        r"jams\s+arbitration\s+rules|jams\s+rules|international\s+arbitration\s+rules)\b",
        lower,
    )
    # Check for cross-border signals (foreign parties, governing laws, etc.)
    # Exclude common US domestic patterns: "governed by [US state] law" /
    # "laws of the State of X" / "laws of X, United States"
    has_international_signal = re.search(
        r"\b(international|cross.border|foreign)\b"
        r"|governed by the laws of (?!the state|[a-z]+ state|[a-z]+,?\s+united states)"
        r"(?![a-z]+\s+law\b)",
        lower,
    )
    if not has_explicit_rules:
        flags.append(Flag(
            category="Defective Rule Selection — institutional rules not specified",
            severity="medium",
            message=(
                "The clause names JAMS as the administering institution but does "
                "not specify which JAMS rule set applies. JAMS operates two "
                "distinct rule sets: the JAMS Comprehensive Arbitration Rules & "
                "Procedures (US domestic default, applies automatically to claims "
                "over $250,000 when no rules are specified) and the JAMS "
                "International Arbitration Rules (designed for cross-border "
                "disputes). For international contracts, specify explicitly: "
                "'...administered by JAMS in accordance with the JAMS "
                "International Arbitration Rules.' Relying on the Comprehensive "
                "Rules default in a cross-border context can produce unexpected "
                "procedural results, particularly on discovery scope and "
                "arbitrator appointment process."
            ),
        ))
    elif has_explicit_rules and has_international_signal:
        # Check whether they've specified Comprehensive Rules in an
        # apparently international contract
        uses_comprehensive = re.search(r"jams\s+comprehensive|comprehensive\s+arbitration\s+rules", lower)
        if uses_comprehensive:
            flags.append(Flag(
                category="Defective Rule Selection — domestic rules incorrectly applied",
                severity="medium",
                message=(
                    "The clause specifies the JAMS Comprehensive Arbitration Rules "
                    "in what appears to be an international contract. The JAMS "
                    "Comprehensive Rules were designed primarily for US domestic "
                    "disputes. For cross-border contracts, JAMS recommends its "
                    "International Arbitration Rules, which follow international "
                    "norms on discovery, confidentiality, and arbitrator appointment. "
                    "Consider substituting 'JAMS International Arbitration Rules' "
                    "unless the Comprehensive Rules are intentionally preferred."
                ),
            ))
    return flags


def check_aaa_rule_set(text: str) -> List[Flag]:
    """AAA-specific check: the American Arbitration Association operates
    separate rule sets for domestic and international disputes:
      - AAA Commercial Arbitration Rules (domestic US)
      - AAA International Arbitration Rules / ICDR Rules (international)
    Cross-border contracts that specify AAA Commercial Rules rather than
    AAA International Rules (administered through AAA's international arm,
    ICDR) may find themselves in procedurally inappropriate proceedings."""
    flags = []
    lower = text.lower()
    has_aaa = "american arbitration association" in lower or (
        re.search(r"\baaa\b", lower) and "arbitrat" in lower
    )
    if not has_aaa:
        return flags
    has_international_signal = re.search(
        r"\b(international|cross.border|icdr)\b"
        r"|governed by the laws of (?!the state|[a-z]+ state|[a-z]+,?\s+united states)",
        lower,
    )
    uses_commercial_rules = re.search(
        r"\b(commercial arbitration rules|aaa commercial)\b", lower
    )
    uses_international_rules = re.search(
        r"\b(international arbitration rules|icdr rules|aaa international)\b", lower
    )
    if has_international_signal and uses_commercial_rules and not uses_international_rules:
        flags.append(Flag(
            category="Defective Rule Selection — domestic rules incorrectly applied",
            severity="medium",
            message=(
                "The clause specifies the AAA Commercial Arbitration Rules in "
                "what appears to be an international contract. For cross-border "
                "disputes, the AAA's international arm (ICDR -- International "
                "Centre for Dispute Resolution) administers proceedings under the "
                "ICDR International Arbitration Rules, which are better suited to "
                "multinational disputes. Consider replacing 'AAA Commercial "
                "Arbitration Rules' with 'ICDR International Arbitration Rules' "
                "or 'AAA International Arbitration Rules' for cross-border "
                "contracts."
            ),
        ))
    return flags


def check_missing_language(text: str) -> List[Flag]:
    """Missing language of arbitration in international contracts.
    Absent an express language clause, the institution or tribunal must
    decide — a process that can take months and generate substantial
    translation costs, particularly in cross-border disputes."""
    flags = []
    lower = text.lower()
    has_arbitration = re.search(r"\barbitrat", lower)
    if not has_arbitration:
        return flags
    has_language = re.search(
        r"language of (the )?(arbitration|proceedings)"
        r"|(the )?language (of .{0,25})?shall be (english|french|chinese|spanish|german|arabic|japanese|korean)"
        r"|(arbitration|proceedings?) shall be (conducted|held) in (english|french|chinese|spanish|german|arabic|japanese|korean)"
        r"|conducted in (english|french|chinese|spanish|german|arabic|japanese|korean)"
        r"|proceedings shall be in (english|french|chinese|spanish|german|arabic|japanese|korean)",
        lower,
    )
    has_international_signal = re.search(
        r"\b(international|cross.border|foreign)\b"
        r"|governed by (the laws of|[a-z]+ law\b)(?! (the state|[a-z]+ state))",
        lower,
    )
    if has_international_signal and not has_language:
        flags.append(Flag(
            category="Missing Procedural Elements — language of arbitration not specified",
            severity="low",
            message=(
                "The clause does not specify the language of arbitration. In "
                "international contracts this omission is a common source of "
                "procedural delay: the tribunal must determine the language "
                "before substantive proceedings can begin, generating translation "
                "costs and potentially months of preliminary dispute. Best "
                "practice is to state explicitly, e.g. 'The language of the "
                "arbitration shall be English.'"
            ),
        ))
    return flags


def check_unilateral_option_clause(text: str) -> List[Flag]:
    """Asymmetric/unilateral option clauses — one party retains the right
    to choose between arbitration and litigation while the other is bound
    exclusively to one forum. These clauses are void or challengeable in
    several jurisdictions (including PRC, France post-2012, and others)
    on grounds of inequality or lack of mutuality."""
    flags = []
    lower = text.lower()
    # Detect patterns where only one named party (lender, bank, company)
    # has the option to elect forum
    patterns = [
        r"\bonly (the )?(lender|bank|company|seller|licensor|franchisor)\b.{0,60}"
        r"\b(may elect|may submit|may choose|may opt|at (its|their) option)\b",
        r"\b(lender|bank|company|seller|licensor|franchisor).{0,40}"
        r"\b(may elect|at (its|their) (sole )?option|may choose)\b.{0,60}"
        r"\b(arbitrat|litigat|court)",
        r"\b(borrower|customer|counterparty|buyer|licensee).{0,60}"
        r"\b(exclusive(ly)?|sole(ly)?|only|shall not have the right)\b.{0,40}"
        r"\b(arbitrat|court|litigat)",
        # "the Bank alone shall have the right to elect court proceedings"
        r"\b(lender|bank|company|seller|licensor|franchisor|supplier)\b.{0,10}"
        r"\balone shall have the right\b.{0,40}\b(court|litigat|elect)",
        # "the Licensor reserves the right to seek relief in the courts"
        r"\b(lender|bank|company|seller|licensor|franchisor|supplier)\b.{0,15}"
        r"\breserves? the right\b.{0,40}\b(court|litigat|relief|proceedings)",
        # "the Supplier may at its sole discretion commence proceedings in any court"
        r"\b(lender|bank|company|seller|licensor|franchisor|supplier)\b.{0,15}"
        r"\bmay at (its|their) sole discretion\b.{0,40}\b(court|proceedings|litigat)",
    ]
    for p in patterns:
        m = re.search(p, lower)
        if m:
            flags.append(Flag(
                category="Structural Defects — unilateral option clause",
                severity="medium",
                message=(
                    "The clause appears to grant only one party the right to "
                    "elect between arbitration and litigation, while the other "
                    "party is bound to a single forum. Such asymmetric clauses "
                    "are void or voidable in several jurisdictions (including "
                    "France post-Rothschild 2012, PRC, and certain EU member "
                    "states) on grounds of inequality or lack of mutuality. "
                    "Even where enforceable, they create a strategic imbalance "
                    "that may be challenged at the enforcement stage."
                ),
                matched_text=m.group(0)[:80],
            ))
            break
    return flags


def check_multi_tier_no_trigger(text: str) -> List[Flag]:
    """Multi-tiered dispute resolution clauses (negotiation/mediation
    before arbitration) without a clear, objective trigger for when the
    pre-arbitral stage has failed. Absent a defined failure point, the
    respondent can object to jurisdiction on the grounds that the condition
    precedent to arbitration has not been satisfied."""
    flags = []
    lower = text.lower()
    # Detect pre-arbitral steps
    has_pre_step = re.search(
        r"\b(amicable(ly)?|friendly negotiation|good faith|senior management|"
        r"negotiat|mediat|conciliat)\b.{0,200}\barbitrat",
        lower,
    )
    if not has_pre_step:
        has_pre_step = re.search(
            r"\b(shall first|first be referred|first attempt"
            r"|prior to (initiating |commencing )?arbitrat)\b",
            lower,
        )
    if not has_pre_step:
        return flags
    # Check for a defined time period or objective failure criterion
    has_trigger = re.search(
        r"\b\d+\s+days?\b"
        r"|such (longer )?period.{0,20}agree.{0,20}writing"
        r"|failing (resolution|agreement|settlement)"
        r"|no agreement is reached"
        r"|upon (expiry|expiration)"
        r"|written notice.{0,30}(fail|unsuccess)"
        r"|within\s+\d+\s+days?"
        r"|mediator.{0,20}certif",
        lower,
    )
    if not has_trigger:
        flags.append(Flag(
            category="Structural Defects — multi-tier clause without defined trigger",
            severity="medium",
            message=(
                "The clause requires a pre-arbitral step (negotiation or "
                "mediation) before arbitration may be commenced, but does not "
                "define an objective trigger for when that step has failed — "
                "e.g. a specific number of days, a written declaration of "
                "impasse, or a mediator's certificate. Without a defined failure "
                "point, a respondent can object to jurisdiction on the basis "
                "that the condition precedent to arbitration has not been "
                "satisfied, potentially generating a preliminary jurisdictional "
                "challenge before substantive proceedings even begin."
            ),
        ))
    return flags


def check_unworkable_tribunal_size(text: str) -> List[Flag]:
    """Even-numbered tribunals (2 or 4 arbitrators) create deadlock risk
    because there is no casting vote. Two-arbitrator tribunals are not
    recognised by any major institutional rules and will require the
    appointment of a third (chair) arbitrator, defeating the clause's
    intent. Four-arbitrator clauses are similarly inoperable."""
    flags = []
    lower = text.lower()
    has_arbitration = re.search(r"\barbitrat", lower)
    if not has_arbitration:
        return flags
    even_number = re.search(
        r"\b(two|2)\s+arbitrators?\b"
        r"|\btribunal shall (be composed of|consist of)\s+(two|2)\b"
        r"|\b(four|4)\s+arbitrators?\b"
        r"|\beach party shall appoint (one|1).{0,30}two arbitrators\b",
        lower,
    )
    if even_number:
        flags.append(Flag(
            category="Missing Procedural Elements — unworkable tribunal composition (even number)",
            severity="medium",
            message=(
                "The clause specifies an even number of arbitrators. "
                "Even-numbered tribunals create deadlock risk because there "
                "is no casting vote: if the two (or four) arbitrators cannot "
                "agree, no award can be rendered. No major institutional rules "
                "recognise two-arbitrator tribunals — under ICC, LCIA, SIAC and "
                "HKIAC rules, an even-numbered panel triggers automatic "
                "appointment of a presiding arbitrator, which may not reflect "
                "the parties' intentions and adds cost. Specify one or three "
                "arbitrators."
            ),
            matched_text=even_number.group(0),
        ))
    return flags


ALL_CHECKS = [
    check_optional_language,
    check_multi_tier_conflict,
    check_institution_rules_mismatch,
    check_garbled_institution_name,
    check_missing_seat,
    check_missing_governing_law,
    check_vague_scope,
    check_number_of_arbitrators,
    check_jams_international_rule_set,
    check_aaa_rule_set,
    check_missing_language,
    check_unilateral_option_clause,
    check_multi_tier_no_trigger,
    check_unworkable_tribunal_size,
]


def analyze_clause(text: str) -> AnalysisResult:
    """Run all pathology checks on a clause and return a structured result."""
    result = AnalysisResult(clause=text)
    for check in ALL_CHECKS:
        result.flags.extend(check(text))
    return result
