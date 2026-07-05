"""
Expanded labeled dataset for training a supervised classifier.
Each entry is (clause_text, label) where label is:
  1 = pathological (exhibits at least one known drafting defect)
  0 = healthy (well-drafted, standard-form clause)

These are hand-constructed variations modeled on standard institutional
model clauses (ICC, LCIA, SIAC, HKIAC, AAA, UNCITRAL) and on patterns
discussed in arbitration literature on pathological clauses. They are
NOT scraped from real contracts (most real contracts are confidential);
this is a constructed dataset for methodology demonstration.
"""

TRAINING_DATA = [
    # ---- Healthy clauses (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement, including any question regarding its existence, validity or termination, shall be referred to and finally resolved by arbitration administered by the International Chamber of Commerce in accordance with the ICC Rules of Arbitration. The seat of arbitration shall be Paris, France. The tribunal shall consist of three arbitrators. The language of arbitration shall be English. This Agreement shall be governed by the laws of England and Wales.", 0),
    ("All disputes arising out of or in connection with this contract shall be finally settled under the Rules of Arbitration of the International Chamber of Commerce by one or more arbitrators appointed in accordance with the said Rules. The seat of arbitration shall be Geneva, Switzerland and the language shall be English. This contract is governed by Swiss law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally resolved by arbitration in accordance with the LCIA Arbitration Rules. The number of arbitrators shall be one. The seat of arbitration shall be London. The language of the arbitration shall be English. The governing law of this contract shall be the laws of England and Wales.", 0),
    ("Any dispute arising from or in connection with this Agreement shall be referred to and finally resolved by arbitration administered by the Singapore International Arbitration Centre in accordance with the Arbitration Rules of the Singapore International Arbitration Centre for the time being in force. The seat of arbitration shall be Singapore. The tribunal shall consist of one arbitrator. The language shall be English. This agreement shall be governed by the laws of Singapore.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be settled by arbitration administered by the Hong Kong International Arbitration Centre under the HKIAC Administered Arbitration Rules. The seat of arbitration shall be Hong Kong. The number of arbitrators shall be three. The arbitration proceedings shall be conducted in English. This Agreement is governed by the laws of Hong Kong.", 0),
    ("Any controversy or claim arising out of or relating to this contract shall be finally settled by arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat of arbitration shall be New York, New York. There shall be one arbitrator. This Agreement shall be governed by the laws of the State of New York.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract, or the breach, termination or invalidity thereof, shall be settled by arbitration in accordance with the UNCITRAL Arbitration Rules, administered by the Permanent Court of Arbitration. The seat of arbitration shall be The Hague, Netherlands. The number of arbitrators shall be three. This Agreement shall be governed by the laws of the Netherlands.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the China International Economic and Trade Arbitration Commission in accordance with its arbitration rules. The seat of arbitration shall be Beijing. The arbitration shall be conducted in English. This Agreement shall be governed by the laws of the People's Republic of China.", 0),
    ("All disputes arising out of or in connection with the present contract shall be finally settled under the Rules of the Stockholm Chamber of Commerce by a sole arbitrator appointed in accordance with the said rules. The seat of arbitration shall be Stockholm. The language of the proceedings shall be English. This Agreement shall be governed by Swedish law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the ICC in accordance with the Rules of Arbitration of the International Chamber of Commerce. The seat shall be Singapore. There shall be three arbitrators. The language shall be English. This Agreement is governed by the laws of Singapore.", 0),
    ("Any claim or dispute arising out of or relating to this Agreement shall be finally settled by binding arbitration administered by the LCIA in accordance with the LCIA Rules. The seat of the arbitration shall be Dubai, UAE. The tribunal shall consist of one arbitrator. The governing law of this Agreement shall be the laws of the DIFC.", 0),
    ("Any dispute shall be finally resolved by arbitration under the SIAC Rules administered by SIAC. The seat of arbitration shall be Singapore. The tribunal shall be composed of three arbitrators. This Agreement shall be governed by Singapore law.", 0),
    ("All disputes arising out of this Agreement shall be referred to and finally resolved by arbitration administered by the HKIAC under the UNCITRAL Arbitration Rules, with HKIAC acting as appointing authority and administering the arbitration. The seat shall be Hong Kong. This Agreement is governed by Hong Kong law.", 0),
    ("Any dispute arising out of or in connection with this contract, including any question regarding its existence, validity or termination, shall be finally resolved by arbitration administered by the ICC in accordance with the ICC Rules. The seat of arbitration shall be Hong Kong and the language of arbitration shall be English. This contract is governed by the laws of Hong Kong.", 0),
    ("Any dispute arising under or related to this Agreement shall be exclusively and finally resolved by binding arbitration administered by the AAA under its International Arbitration Rules. The seat shall be Chicago, Illinois. The tribunal shall consist of one arbitrator. This Agreement is governed by Illinois law.", 0),

    # ---- Pathological: optional language (label 1) ----
    ("In the event of a dispute, either party may submit the matter to arbitration under the Rules of the International Chamber of Commerce.", 1),
    ("Should any dispute arise, the parties may refer such dispute to arbitration administered by the LCIA in accordance with the LCIA Rules.", 1),
    ("If a dispute arises under this Agreement, either party may elect to refer the dispute to arbitration under the SIAC Rules.", 1),
    ("Any dispute arising hereunder might be submitted by either party to arbitration administered by HKIAC.", 1),
    ("The parties may choose to submit any dispute arising out of this contract to arbitration under the ICC Rules of Arbitration in Paris.", 1),
    ("In case of a dispute, either party may refer the matter to binding arbitration administered by the AAA under its Commercial Rules.", 1),

    # ---- Pathological: institution-rules mismatch (label 1) ----
    ("Any dispute shall be finally settled by arbitration administered by the Singapore International Arbitration Centre in accordance with the UNCITRAL Arbitration Rules. The seat of arbitration shall be Singapore.", 1),
    ("All disputes shall be referred to arbitration administered by HKIAC under the UNCITRAL Arbitration Rules. The seat shall be Hong Kong.", 1),
    ("Any controversy shall be finally resolved by arbitration administered by the ICC under the UNCITRAL Arbitration Rules. The seat shall be Paris.", 1),
    ("Disputes arising out of this Agreement shall be settled by arbitration administered by CIETAC under the UNCITRAL Arbitration Rules. The seat shall be Beijing.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the LCIA under the UNCITRAL Arbitration Rules. The seat shall be London.", 1),

    # ---- Pathological: conflicting mechanisms (label 1) ----
    ("Any dispute arising under this Agreement may be referred to arbitration. Notwithstanding the foregoing, either party may also bring an action before a court of competent jurisdiction.", 1),
    ("Disputes shall be resolved by arbitration administered by the ICC. However, nothing in this clause shall prevent either party from initiating litigation in any court of competent jurisdiction at any time.", 1),
    ("The parties agree to submit disputes to arbitration under the LCIA Rules, provided that either party may instead bring a lawsuit in the courts of New York if it so chooses.", 1),
    ("Any dispute may be resolved through arbitration under the SIAC Rules or, alternatively, either party may pursue a civil action in a court of competent jurisdiction.", 1),
    ("Disputes arising out of this Agreement shall be subject to arbitration administered by HKIAC. The parties also reserve the right to bring any claim before the courts of Hong Kong at their discretion.", 1),

    # ---- Pathological: garbled / unrecognized institution name (label 1) ----
    ("Any dispute shall be finally resolved by arbitration administered by the International Arbitration Commission of Singapore in accordance with its rules. The seat of arbitration shall be Singapore.", 1),
    ("All disputes shall be referred to arbitration administered by the Asia Pacific Arbitration Court under its applicable rules. The seat shall be Hong Kong.", 1),
    ("Any controversy shall be finally settled by arbitration administered by the Global Commercial Arbitration Institute. The seat shall be New York.", 1),
    ("Disputes arising hereunder shall be resolved by arbitration administered by the United Nations Arbitration Chamber under its rules. The seat shall be Geneva.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the World Trade Arbitration Association in accordance with its arbitration rules. The seat shall be London.", 1),

    # ---- Pathological: missing seat / governing law (label 1) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the International Chamber of Commerce in accordance with the ICC Rules of Arbitration. The tribunal shall consist of one arbitrator.", 1),
    ("All disputes shall be referred to and finally resolved by arbitration administered by the LCIA under the LCIA Rules. The number of arbitrators shall be three.", 1),
    ("Any controversy or claim arising out of this contract shall be settled by arbitration administered by SIAC under the SIAC Rules. The tribunal shall consist of one arbitrator.", 1),
    ("Disputes arising hereunder shall be finally resolved by arbitration administered by HKIAC under the HKIAC Rules. The arbitration shall be conducted in English.", 1),
    ("Any dispute shall be finally settled by arbitration administered by the AAA under its Commercial Arbitration Rules. The tribunal shall consist of three arbitrators.", 1),

    # ---- Pathological: vague scope only, otherwise complete (label 1) ----
    ("Disputes shall be finally resolved by arbitration administered by the ICC under the ICC Rules. The seat of arbitration shall be Paris. The tribunal shall consist of one arbitrator. This Agreement is governed by French law.", 1),
    ("Disagreements between the parties under this contract shall be settled by arbitration administered by LCIA under the LCIA Rules. The seat shall be London. The tribunal shall consist of one arbitrator. This Agreement is governed by English law.", 1),
    ("Any matter in dispute shall be resolved by arbitration administered by SIAC under the SIAC Rules. The seat shall be Singapore. There shall be one arbitrator. This Agreement is governed by Singapore law.", 1),

    # ---- Pathological: combined multiple defects (label 1) ----
    ("If a dispute arises, either party may submit the matter to the International Arbitration Council for resolution. Alternatively, either party may pursue litigation in any court it deems appropriate.", 1),
    ("Should any controversy arise, the parties may refer the matter to arbitration administered by the Global Dispute Resolution Centre under the UNCITRAL Rules, or alternatively bring suit in court.", 1),

    # ============================================================
    # Extended set -- additional institutions, phrasings, and
    # combinations to broaden coverage beyond the original 46.
    # ============================================================

    # ---- Healthy clauses (label 0), more institutions and styles ----
    ("Any dispute arising out of or relating to this contract, including the breach, termination or invalidity thereof, shall be finally settled by arbitration administered by the German Arbitration Institute (DIS) in accordance with its Arbitration Rules. The seat of arbitration shall be Frankfurt am Main, Germany. The number of arbitrators shall be three. The language of the arbitration shall be English. This Agreement shall be governed by German law.", 0),
    ("Any dispute arising out of or in connection with this contract shall be referred to and finally resolved by arbitration administered by the Japan Commercial Arbitration Association under its Commercial Arbitration Rules. The seat of arbitration shall be Tokyo, Japan. The tribunal shall consist of one arbitrator. The language shall be English. This Agreement is governed by Japanese law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally resolved by arbitration administered by the Korean Commercial Arbitration Board in accordance with its International Arbitration Rules. The seat shall be Seoul, Republic of Korea. The number of arbitrators shall be one. This Agreement shall be governed by the laws of the Republic of Korea.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be referred to and finally resolved by arbitration administered by the Dubai International Arbitration Centre in accordance with the DIAC Arbitration Rules. The seat of arbitration shall be the Dubai International Financial Centre. The tribunal shall consist of three arbitrators. The language shall be English. This Agreement shall be governed by the laws of the DIFC.", 0),
    ("Any dispute arising out of or relating to this Agreement shall be finally settled by arbitration administered by the Vienna International Arbitral Centre under the Vienna Rules. The seat of arbitration shall be Vienna, Austria. The number of arbitrators shall be one. This Agreement is governed by Austrian law.", 0),
    ("Any dispute, controversy or claim arising out of or in connection with this contract shall be finally resolved by arbitration administered by the Australian Centre for International Commercial Arbitration under its Rules. The seat of arbitration shall be Sydney, Australia. There shall be three arbitrators. The language of arbitration shall be English. This Agreement is governed by the laws of New South Wales.", 0),
    ("Any controversy arising out of or relating to this contract shall be finally settled by arbitration administered by the International Centre for Dispute Resolution in accordance with its International Dispute Resolution Procedures. The seat of arbitration shall be Miami, Florida. The tribunal shall consist of one arbitrator. This Agreement shall be governed by Florida law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the Cairo Regional Centre for International Commercial Arbitration in accordance with its rules. The seat of arbitration shall be Cairo, Egypt. The number of arbitrators shall be three. The language shall be English. This Agreement is governed by Egyptian law.", 0),
    ("Any dispute arising out of or relating to this contract shall be referred to and finally resolved by arbitration administered by the Milan Chamber of Arbitration under its Arbitration Rules. The seat of arbitration shall be Milan, Italy. The tribunal shall consist of one arbitrator. This Agreement shall be governed by Italian law.", 0),
    ("Any dispute, controversy or claim arising out of or in connection with this Agreement shall be finally settled by arbitration administered by the China International Economic and Trade Arbitration Commission South China Sub-Commission in accordance with the CIETAC Arbitration Rules. The seat of arbitration shall be Shenzhen. The tribunal shall consist of three arbitrators. The language shall be English. This Agreement is governed by the laws of the People's Republic of China.", 0),
    ("Any dispute arising out of or in connection with this contract shall be finally resolved by arbitration administered by the Beijing Arbitration Commission in accordance with its Arbitration Rules. The seat of arbitration shall be Beijing. The number of arbitrators shall be one. The language of the arbitration shall be Chinese and English. This Agreement is governed by the laws of the People's Republic of China.", 0),
    ("All disputes arising from or in connection with this contract shall be submitted to the Shanghai International Arbitration Centre for arbitration in accordance with its arbitration rules. The seat of arbitration shall be Shanghai. The tribunal shall be composed of three arbitrators. This Agreement is governed by the laws of the People's Republic of China.", 0),
    ("Any dispute arising out of or relating to this Agreement, including any question regarding its existence, validity, or termination, shall be referred to and finally resolved by arbitration administered by the ICC in accordance with the Rules of Arbitration of the International Chamber of Commerce, which Rules are deemed to be incorporated by reference into this clause. The seat of arbitration shall be Geneva. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement shall be governed by the substantive laws of Switzerland.", 0),
    ("Any dispute arising under or in connection with this Agreement shall be finally resolved by arbitration administered by SIAC in accordance with the Arbitration Rules of the Singapore International Arbitration Centre, which rules are deemed incorporated by reference. The seat of the arbitration shall be Singapore. The arbitral tribunal shall consist of one arbitrator appointed in accordance with the said rules. The language of the arbitration shall be English. This Agreement shall be governed by and construed in accordance with the laws of Singapore.", 0),
    ("Any and all disputes arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by HKIAC in accordance with the HKIAC Administered Arbitration Rules in force when the Notice of Arbitration is submitted. The seat of arbitration shall be Hong Kong. The number of arbitrators shall be three. The language to be used in the arbitral proceedings shall be English. This Agreement shall be governed by the laws of the Hong Kong Special Administrative Region.", 0),
    ("Any dispute arising out of this Agreement shall be referred to arbitration administered by CIETAC under the UNCITRAL Arbitration Rules, with CIETAC acting as the appointing authority and providing administrative support in accordance with its Guidelines on Administering Cases under the UNCITRAL Arbitration Rules. The seat of arbitration shall be Beijing. This Agreement is governed by the laws of the People's Republic of China.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be referred to and finally resolved by ad hoc arbitration conducted in accordance with the UNCITRAL Arbitration Rules. The appointing authority shall be the Permanent Court of Arbitration. The seat of arbitration shall be The Hague. The tribunal shall consist of three arbitrators. This Agreement is governed by Dutch law.", 0),

    # ---- Pathological: optional language, more variants (label 1) ----
    ("Either party may, at its discretion, submit any dispute arising under this Agreement to arbitration administered by the DIS under the DIS Rules.", 1),
    ("In the event a dispute cannot be resolved amicably, either party may elect to commence arbitration administered by JCAA under its Commercial Arbitration Rules.", 1),
    ("The parties may, but are not obligated to, refer any dispute arising hereunder to arbitration administered by KCAB under its International Arbitration Rules.", 1),
    ("If the parties fail to resolve a dispute through negotiation, either party may, at its option, initiate arbitration administered by DIAC under the DIAC Rules.", 1),
    ("Either party may submit any controversy arising out of this contract to binding arbitration under the Vienna Rules administered by VIAC.", 1),
    ("The parties hereto may agree to refer any dispute to arbitration administered by the Beijing Arbitration Commission under its rules.", 1),

    # ---- Pathological: institution-rules mismatch, more variants (label 1) ----
    ("Any dispute shall be finally resolved by arbitration administered by the Japan Commercial Arbitration Association under the UNCITRAL Arbitration Rules. The seat shall be Tokyo.", 1),
    ("All disputes shall be referred to arbitration administered by the Korean Commercial Arbitration Board under the UNCITRAL Arbitration Rules. The seat shall be Seoul.", 1),
    ("Any controversy shall be finally resolved by arbitration administered by the Dubai International Arbitration Centre under the UNCITRAL Arbitration Rules. The seat shall be Dubai.", 1),
    ("Any dispute shall be finally settled by arbitration administered by the Beijing Arbitration Commission under the UNCITRAL Arbitration Rules. The seat shall be Beijing.", 1),
    ("Disputes arising out of this Agreement shall be settled by arbitration administered by the Vienna International Arbitral Centre under the UNCITRAL Arbitration Rules. The seat shall be Vienna.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the Shanghai International Arbitration Centre under the UNCITRAL Arbitration Rules. The seat shall be Shanghai.", 1),

    # ---- Pathological: conflicting mechanisms, more variants (label 1) ----
    ("Disputes shall first be referred to arbitration administered by the DIS. Notwithstanding the foregoing, either party retains the right to seek relief in any court of competent jurisdiction at any time.", 1),
    ("Any controversy shall be submitted to arbitration under the JCAA Commercial Arbitration Rules; provided, however, that either party may bring a claim in the courts of Tokyo instead if it prefers.", 1),
    ("The parties agree that disputes shall be resolved by arbitration administered by the KCAB, without prejudice to either party's right to commence litigation in the courts of Seoul.", 1),
    ("Disputes arising under this Agreement shall be referred to arbitration under the DIAC Rules, or alternatively, either party may initiate proceedings before the courts of Dubai.", 1),
    ("Any dispute shall be resolved through arbitration administered by the Beijing Arbitration Commission. This shall not preclude either party from filing a lawsuit in a people's court of competent jurisdiction.", 1),

    # ---- Pathological: garbled / unrecognized institution name, more variants (label 1) ----
    ("Any dispute shall be finally resolved by arbitration administered by the East Asia Commercial Arbitration Bureau in accordance with its rules. The seat shall be Tokyo.", 1),
    ("All disputes shall be referred to arbitration administered by the Pacific Rim Arbitration Tribunal under its applicable rules. The seat shall be Seoul.", 1),
    ("Any controversy shall be finally settled by arbitration administered by the Middle East Commercial Arbitration Authority. The seat shall be Dubai.", 1),
    ("Disputes arising hereunder shall be resolved by arbitration administered by the China Trade Arbitration Office under its rules. The seat shall be Shanghai.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the European Business Arbitration Bureau in accordance with its arbitration rules. The seat shall be Vienna.", 1),
    ("All disputes arising out of this Agreement shall be submitted to the International Trade Dispute Centre for arbitration under its rules. The seat shall be New York.", 1),

    # ---- Pathological: missing seat / governing law, more variants (label 1) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the DIS in accordance with the DIS Arbitration Rules. The tribunal shall consist of three arbitrators.", 1),
    ("All disputes shall be referred to and finally resolved by arbitration administered by the JCAA under its Commercial Arbitration Rules. The number of arbitrators shall be one.", 1),
    ("Any controversy or claim arising out of this contract shall be settled by arbitration administered by the KCAB under its International Arbitration Rules. The tribunal shall consist of one arbitrator.", 1),
    ("Disputes arising hereunder shall be finally resolved by arbitration administered by DIAC under the DIAC Rules. The arbitration shall be conducted in English.", 1),
    ("Any dispute shall be finally settled by arbitration administered by the Beijing Arbitration Commission under its rules. The tribunal shall consist of three arbitrators.", 1),
    ("Any dispute arising out of this contract shall be resolved by arbitration administered by the Shanghai International Arbitration Centre. The tribunal shall be composed of one arbitrator.", 1),

    # ---- Pathological: vague scope, more variants (label 1) ----
    ("Disputes shall be finally resolved by arbitration administered by the DIS under the DIS Rules. The seat of arbitration shall be Frankfurt. The tribunal shall consist of one arbitrator. This Agreement is governed by German law.", 1),
    ("Disagreements between the parties shall be settled by arbitration administered by JCAA under its rules. The seat shall be Tokyo. The tribunal shall consist of one arbitrator. This Agreement is governed by Japanese law.", 1),
    ("Any matter in dispute shall be resolved by arbitration administered by the Beijing Arbitration Commission under its rules. The seat shall be Beijing. There shall be one arbitrator. This Agreement is governed by Chinese law.", 1),

    # ---- Pathological: combined multiple defects, more variants (label 1) ----
    ("If any dispute arises, either party may submit the matter to the Asia Commercial Resolution Bureau for resolution. Alternatively, either party may pursue litigation in any court it deems appropriate.", 1),
    ("Should any controversy arise, the parties may refer the matter to arbitration administered by the World Commercial Arbitration Forum under the UNCITRAL Rules, or alternatively bring suit in court.", 1),
    ("Either party may submit any dispute to the Pacific Trade Arbitration Council for resolution. The Council shall apply the UNCITRAL Arbitration Rules, but either party may also commence litigation at any time.", 1),
    ("In case of dispute, either party may, at its sole discretion, refer the matter to the Global Commercial Arbitration Institute or alternatively file suit in a court of competent jurisdiction.", 1),

    # ============================================================
    # AAA / ICDR extended coverage
    # ============================================================

    # ---- Healthy: AAA domestic (Commercial Rules, US seat) (label 0) ----
    ("Any controversy or claim arising out of or relating to this contract, or the breach, termination or invalidity thereof, shall be finally settled by arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat of arbitration shall be Houston, Texas. There shall be one arbitrator. This Agreement is governed by the laws of Texas.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the AAA under its Commercial Arbitration Rules. The seat of arbitration shall be Los Angeles, California. The number of arbitrators shall be three. This Agreement is governed by California law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this Agreement shall be submitted to binding arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat shall be Atlanta, Georgia. The tribunal shall consist of one arbitrator. This Agreement is governed by Georgia law.", 0),

    # ---- Healthy: AAA/ICDR international (International Rules, non-US seat or cross-border) (label 0) ----
    ("Any dispute arising out of or in connection with this contract shall be finally resolved by arbitration administered by the International Centre for Dispute Resolution (ICDR) in accordance with its International Arbitration Rules. The seat of arbitration shall be New York, New York. The tribunal shall consist of three arbitrators. The language of arbitration shall be English. This Agreement shall be governed by the laws of the State of New York.", 0),
    ("Any dispute arising out of or relating to this Agreement shall be finally settled by arbitration administered by the American Arbitration Association under its International Arbitration Rules. The seat of arbitration shall be Miami, Florida. The number of arbitrators shall be one. The language of arbitration shall be English. This Agreement is governed by Florida law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the ICDR in accordance with the ICDR International Arbitration Rules. The seat of arbitration shall be New York. The tribunal shall consist of three arbitrators. This Agreement is governed by the laws of England and Wales.", 0),

    # ---- Pathological: AAA Commercial Rules in international contract (label 1) ----
    ("Any international dispute arising under this Agreement shall be resolved by arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat shall be New York. The laws of England and Wales govern this Agreement.", 1),
    ("Any dispute arising out of this cross-border Agreement shall be finally settled by arbitration administered by the AAA under its Commercial Arbitration Rules. The seat shall be Miami. This Agreement is governed by the laws of Switzerland.", 1),
    ("Any dispute arising out of this international contract shall be submitted to arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat shall be Houston. This Agreement is governed by the laws of Singapore.", 1),

    # ---- Pathological: AAA optional/conflicting/garbled (label 1) ----
    ("Either party may, in its discretion, submit any dispute to the American Arbitration Association for arbitration under its Commercial Arbitration Rules.", 1),
    ("Any dispute may be resolved by arbitration under the AAA Rules or, alternatively, litigated in any court of competent jurisdiction.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the National Arbitration Association under its applicable rules. The seat shall be New York.", 1),

    # ============================================================
    # JAMS extended coverage
    # ============================================================

    # ---- Healthy: JAMS domestic (Comprehensive Rules, US seat) (label 0) ----
    ("Any controversy or claim arising out of or relating to this Agreement, or the breach thereof, shall be settled by arbitration administered by JAMS in accordance with its Comprehensive Arbitration Rules and Procedures. The seat of arbitration shall be San Francisco, California. The tribunal shall consist of one arbitrator. This Agreement is governed by California law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by JAMS under its Comprehensive Arbitration Rules and Procedures. The seat of arbitration shall be New York, New York. The number of arbitrators shall be three. This Agreement is governed by New York law.", 0),
    ("Any dispute, controversy or claim arising under this Agreement shall be settled by binding arbitration administered by JAMS pursuant to its Comprehensive Arbitration Rules and Procedures. The seat shall be Chicago, Illinois. The tribunal shall consist of one arbitrator. This Agreement is governed by Illinois law.", 0),
    ("Any dispute arising out of this Agreement shall be submitted to binding arbitration before JAMS in accordance with its Comprehensive Arbitration Rules and Procedures. The seat shall be Los Angeles, California. There shall be one arbitrator selected in accordance with such rules. This Agreement is governed by California law.", 0),

    # ---- Healthy: JAMS International (International Rules, cross-border) (label 0) ----
    ("Any dispute arising out of or in connection with this contract shall be finally settled by arbitration administered by JAMS in accordance with the JAMS International Arbitration Rules. The seat of arbitration shall be New York, New York. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement is governed by the laws of England and Wales.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this Agreement shall be finally resolved by arbitration administered by JAMS pursuant to the JAMS International Arbitration Rules. The seat of arbitration shall be New York. There shall be one arbitrator. The language of the arbitration shall be English. This Agreement is governed by New York law.", 0),
    ("Any dispute arising out of or relating to this Agreement shall be finally settled by arbitration before JAMS International under the JAMS International Arbitration Rules. The seat of arbitration shall be Miami, Florida. The tribunal shall consist of three arbitrators. This Agreement is governed by Florida law.", 0),

    # ---- Pathological: JAMS -- no rule set specified (label 1) ----
    ("Any dispute arising out of this Agreement shall be submitted to binding arbitration before JAMS. The seat shall be New York. The tribunal shall consist of one arbitrator. This Agreement is governed by New York law.", 1),
    ("Any controversy or claim arising under this Agreement shall be resolved by arbitration administered by JAMS. The seat shall be San Francisco. There shall be one arbitrator.", 1),
    ("All disputes arising out of this Agreement shall be submitted to JAMS for final and binding arbitration. The seat shall be Chicago. This Agreement is governed by Illinois law.", 1),
    ("Any dispute shall be finally resolved by binding arbitration before JAMS. The seat of arbitration shall be Los Angeles. The number of arbitrators shall be three. This Agreement is governed by California law.", 1),

    # ---- Pathological: JAMS Comprehensive Rules in international contract (label 1) ----
    ("Any international dispute arising out of this Agreement shall be finally resolved by arbitration administered by JAMS under its Comprehensive Arbitration Rules and Procedures. The seat shall be New York. This Agreement is governed by the laws of England and Wales.", 1),
    ("Any dispute arising out of this cross-border Agreement shall be settled by arbitration administered by JAMS in accordance with its Comprehensive Arbitration Rules and Procedures. The seat shall be New York. This Agreement is governed by Swiss law.", 1),

    # ---- Pathological: JAMS optional language (label 1) ----
    ("Either party may, at its option, submit any dispute arising under this Agreement to binding arbitration before JAMS under its Comprehensive Arbitration Rules.", 1),
    ("In the event of a dispute, either party may elect to submit the matter to JAMS for arbitration under its rules.", 1),

    # ---- Pathological: JAMS conflicting mechanisms (label 1) ----
    ("Any dispute shall be submitted to arbitration before JAMS under its Comprehensive Rules; provided, however, that either party may also bring any claim in a court of competent jurisdiction if it elects to do so.", 1),
    ("Disputes shall be resolved by JAMS arbitration under its Comprehensive Rules. Nothing herein shall prevent either party from initiating litigation in any court.", 1),

    # ---- Pathological: JAMS garbled name (label 1) ----
    ("Any dispute shall be finally resolved by arbitration administered by the JAMS National Dispute Resolution Association under its applicable rules. The seat shall be New York.", 1),
    ("All disputes shall be submitted to the Joint Arbitration & Mediation Services for final resolution under its rules. The seat shall be San Francisco.", 1),

    # ============================================================
    # AAA / JAMS extended — additional healthy and defective
    # ============================================================

    # ---- Healthy: AAA domestic variants (label 0) ----
    ("Any dispute arising out of or relating to this Agreement shall be resolved by binding arbitration administered by the American Arbitration Association under its Commercial Arbitration Rules. The seat of arbitration shall be Dallas, Texas. The tribunal shall consist of one arbitrator. This Agreement is governed by the laws of Texas.", 0),
    ("All disputes arising out of this Agreement shall be submitted to final and binding arbitration administered by the AAA under its Commercial Arbitration Rules. The seat shall be Boston, Massachusetts. There shall be three arbitrators. This Agreement is governed by Massachusetts law.", 0),
    ("Any controversy or claim arising out of or relating to this contract shall be finally settled by arbitration before the American Arbitration Association under its Employment Arbitration Rules and Mediation Procedures. The seat shall be Seattle, Washington. There shall be one arbitrator. This Agreement is governed by Washington law.", 0),

    # ---- Healthy: JAMS additional domestic variants (label 0) ----
    ("Any controversy or claim arising out of or relating to this Agreement shall be resolved by binding arbitration administered by JAMS pursuant to its Comprehensive Arbitration Rules and Procedures. The seat of arbitration shall be Boston, Massachusetts. The arbitral tribunal shall consist of one arbitrator. This Agreement is governed by Massachusetts law.", 0),
    ("Any dispute, controversy or claim arising out of this Agreement shall be settled by arbitration administered by JAMS under its Comprehensive Arbitration Rules. The seat shall be Houston, Texas. The number of arbitrators shall be three. This Agreement is governed by Texas law.", 0),
    ("Any dispute arising out of or relating to this Agreement shall be finally resolved by arbitration before JAMS pursuant to its Comprehensive Arbitration Rules and Procedures. The seat shall be Washington, D.C. The tribunal shall consist of one arbitrator. This Agreement is governed by the laws of the District of Columbia.", 0),

    # ---- Healthy: JAMS International additional variants (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally settled by arbitration administered by JAMS in accordance with the JAMS International Arbitration Rules. The seat of arbitration shall be London, England. The tribunal shall consist of three arbitrators. The language of arbitration shall be English. This Agreement is governed by the laws of England and Wales.", 0),
    ("Any dispute arising under or relating to this Agreement shall be resolved by arbitration administered by JAMS under the JAMS International Arbitration Rules. The seat of arbitration shall be Singapore. The tribunal shall consist of one arbitrator. This Agreement is governed by Singapore law.", 0),

    # ---- Pathological: AAA additional defects (label 1) ----
    ("Any dispute shall be resolved by arbitration under the AAA Rules. The seat shall be New York. The tribunal shall consist of one arbitrator.", 1),
    ("All disputes shall be submitted to binding arbitration administered by the American Arbitration Association. This Agreement is governed by New York law.", 1),
    ("Any controversy arising under this Agreement may be submitted to the AAA for arbitration, or alternatively resolved through litigation in any court of competent jurisdiction.", 1),
    ("Any dispute arising out of this international Agreement shall be resolved by arbitration administered by the AAA under its Commercial Arbitration Rules. The seat shall be London. This Agreement is governed by English law.", 1),

    # ---- Pathological: JAMS additional defects (label 1) ----
    ("Either party may, in its discretion, elect to submit any dispute to JAMS for resolution under any rules JAMS deems appropriate.", 1),
    ("Any dispute shall be resolved by JAMS. The seat shall be New York. This Agreement is governed by New York law.", 1),
    ("Any international dispute arising under this Agreement shall be resolved by arbitration before JAMS under its Comprehensive Arbitration Rules. The seat shall be New York. This Agreement is governed by German law.", 1),

    # ============================================================
    # Singapore (SIAC / Maxwell Chambers) — extended coverage
    # ============================================================

    # ---- Healthy: SIAC additional variants (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement, including any question regarding its existence, validity or termination, shall be referred to and finally resolved by arbitration administered by the Singapore International Arbitration Centre in accordance with the Arbitration Rules of the Singapore International Arbitration Centre for the time being in force. The seat of arbitration shall be Singapore. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement shall be governed by Singapore law.", 0),
    ("Any dispute arising out of or relating to this contract shall be finally settled by arbitration administered by SIAC in accordance with the SIAC Rules. The seat of arbitration shall be Singapore. There shall be one arbitrator appointed in accordance with the SIAC Rules. The language of arbitration shall be English. This Agreement is governed by the laws of Singapore.", 0),
    ("Any dispute, controversy or claim arising out of this Agreement shall be referred to and finally resolved by arbitration under the SIAC Rules. The seat of arbitration shall be Singapore. The tribunal shall consist of three arbitrators. This Agreement is governed by Singapore law.", 0),

    # ---- Healthy: SICC / Singapore-seated ad hoc (label 0) ----
    ("Any dispute arising out of or in connection with this contract shall be finally resolved by arbitration in accordance with the UNCITRAL Arbitration Rules, administered by the Singapore International Arbitration Centre as the appointing authority. The seat of arbitration shall be Singapore. The tribunal shall consist of three arbitrators. The language shall be English. This Agreement is governed by Singapore law.", 0),

    # ---- Pathological: SIAC defects (label 1) ----
    ("Any dispute shall be finally settled by arbitration under the rules of SIAC. The seat shall be Singapore.", 1),
    ("Either party may submit any dispute to the Singapore International Arbitration Centre for arbitration, or alternatively commence proceedings in the Singapore courts.", 1),
    ("Any dispute arising under this Agreement shall be settled by arbitration administered by the Singapore Arbitration Centre under UNCITRAL Rules. The seat shall be Singapore. This Agreement is governed by Singapore law.", 1),
    ("Any dispute shall be resolved by arbitration administered by SIAC. The seat shall be Singapore. The tribunal shall consist of two arbitrators. This Agreement is governed by Singapore law.", 1),
    ("Any dispute arising under this Agreement may be referred to SIAC for arbitration under the SIAC Rules if the parties so agree at the time the dispute arises.", 1),

    # ============================================================
    # Hong Kong (HKIAC / HKMA) — extended coverage
    # ============================================================

    # ---- Healthy: HKIAC additional variants (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement, including any question regarding its existence, validity or termination, shall be referred to and finally resolved by arbitration administered by the Hong Kong International Arbitration Centre in accordance with the HKIAC Administered Arbitration Rules in force when the Notice of Arbitration is submitted. The seat of arbitration shall be Hong Kong. The tribunal shall consist of three arbitrators. The language shall be English. This Agreement is governed by Hong Kong law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally resolved by arbitration administered by HKIAC under the HKIAC Administered Arbitration Rules. The seat of arbitration shall be Hong Kong. There shall be one arbitrator. The language of the arbitration shall be English. This Agreement is governed by the laws of Hong Kong.", 0),
    ("Any dispute arising under or in connection with this Agreement shall be finally settled by arbitration administered by HKIAC under the HKIAC Administered Arbitration Rules. The seat shall be Hong Kong. The tribunal shall consist of one arbitrator. This Agreement shall be governed by Hong Kong law.", 0),

    # ---- Healthy: HKIAC UNCITRAL (properly administered) (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration in accordance with the UNCITRAL Arbitration Rules, with HKIAC acting as the appointing authority and administering the arbitration under its Guidelines on Administering Cases under UNCITRAL Rules. The seat shall be Hong Kong. The tribunal shall consist of three arbitrators. This Agreement is governed by Hong Kong law.", 0),

    # ---- Pathological: HKIAC defects (label 1) ----
    ("Any dispute shall be settled by arbitration in Hong Kong under the HKIAC Rules.", 1),
    ("Either party may submit any dispute to HKIAC for arbitration, or alternatively to the courts of Hong Kong.", 1),
    ("Any dispute arising under this Agreement shall be settled by arbitration administered by the Hong Kong Arbitration Centre under UNCITRAL Rules. The seat shall be Hong Kong.", 1),
    ("Any dispute arising under this Agreement shall be finally resolved by arbitration administered by HKIAC under the UNCITRAL Arbitration Rules. The seat shall be Hong Kong. This Agreement is governed by Hong Kong law.", 1),
    ("Disputes shall be resolved by arbitration in Hong Kong. The seat shall be Hong Kong. The tribunal shall consist of two arbitrators. This Agreement is governed by Hong Kong law.", 1),

    # ============================================================
    # English arbitration institutions — extended coverage
    # (LCIA, Chartered Institute of Arbitrators, CIArb)
    # ============================================================

    # ---- Healthy: LCIA additional variants (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement, including any question regarding its existence, validity or termination, shall be referred to and finally resolved by arbitration under the LCIA Rules. The number of arbitrators shall be three. The seat of arbitration shall be London. The language of the arbitration shall be English. This Agreement shall be governed by English law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally settled by arbitration administered by the London Court of International Arbitration under its rules. The seat shall be London, England. There shall be one arbitrator. The language of arbitration shall be English. This Agreement is governed by the laws of England and Wales.", 0),
    ("All disputes arising out of or in connection with this Agreement shall be finally resolved by arbitration under the LCIA Arbitration Rules. The seat of arbitration shall be London. The tribunal shall consist of three arbitrators. The arbitration shall be conducted in English. This Agreement is governed by English law.", 0),

    # ---- Pathological: LCIA defects (label 1) ----
    ("Any dispute shall be resolved by arbitration under the rules of the LCIA. The seat shall be London.", 1),
    ("Either party may submit any dispute to LCIA arbitration, or alternatively pursue litigation in the courts of England and Wales.", 1),
    ("Any dispute arising under this Agreement shall be settled by arbitration administered by the LCIA under the UNCITRAL Arbitration Rules. The seat shall be London. This Agreement is governed by English law.", 1),
    ("Any dispute may be submitted to arbitration before the London Court of International Arbitration. The seat shall be London. The tribunal shall consist of two arbitrators. This Agreement is governed by English law.", 1),

    # ============================================================
    # Clauses giving rise to setting-aside / annulment applications
    # and jurisdictional objections
    # ============================================================

    # ---- Pathological: clauses creating grounds for setting aside (label 1) ----

    # Arbitrator-selection mechanism removes party autonomy / creates inequality
    ("Any dispute arising out of this Agreement shall be finally resolved by arbitration administered by the ICC. The respondent shall appoint all three arbitrators. The seat shall be Paris. This Agreement is governed by French law.", 1),

    # Clause purports to make arbitral award subject to court appeal on the merits
    ("Any dispute shall be finally resolved by arbitration administered by the LCIA under the LCIA Rules. The seat shall be London. Either party may appeal the arbitral award to the High Court of England and Wales on any question of law or fact. This Agreement is governed by English law.", 1),

    # Clause purports to require court confirmation before award is enforceable
    ("All disputes shall be finally resolved by arbitration administered by the ICC under its Rules. The seat shall be Paris. The award shall not be enforceable until confirmed by a court of competent jurisdiction. This Agreement is governed by French law.", 1),

    # Clause purports to limit arbitral tribunal's authority to grant interim relief
    ("Any dispute shall be resolved by arbitration administered by SIAC under the SIAC Rules. The seat shall be Singapore. The arbitral tribunal shall have no authority to grant interim measures of protection or emergency relief of any kind. This Agreement is governed by Singapore law.", 1),

    # Clause requires unanimous tribunal decision — creates deadlock risk
    ("Any dispute arising out of this Agreement shall be finally resolved by arbitration administered by the ICC in accordance with the ICC Rules. The seat shall be Paris. The tribunal shall consist of three arbitrators and all decisions shall be by unanimous vote. This Agreement is governed by French law.", 1),

    # Clause sets unrealistic time limit creating due process risk
    ("Any dispute arising under this Agreement shall be finally resolved by arbitration administered by the ICC under its Rules. The seat shall be Geneva. The arbitral tribunal must render its final award within 30 days of the Notice of Arbitration. This Agreement is governed by Swiss law.", 1),

    # ---- Pathological: clauses generating jurisdictional objections (label 1) ----

    # Scope carve-out creates parallel proceedings risk
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the ICC under the ICC Rules, except for disputes relating to intellectual property rights which shall be exclusively submitted to the courts of England and Wales. The seat of arbitration shall be London. This Agreement is governed by English law.", 1),

    # Clause requires pre-arbitral steps but without clear waiver mechanism
    ("Any dispute arising under this Agreement shall be submitted to arbitration administered by LCIA under its rules only after the parties have attempted mediation for a period of not less than six months. No party may commence arbitration without first completing such mediation period. The seat shall be London.", 1),

    # Jurisdiction agreement split across multiple documents with conflicting provisions
    ("Any dispute arising out of the Master Agreement shall be resolved by arbitration administered by the ICC. Any dispute arising out of a Transaction Confirmation shall be resolved in the courts of New York. The seat of arbitration shall be New York. This Agreement is governed by New York law.", 1),

    # Clause selects a seat in a non-New York Convention signatory country
    ("Any dispute arising out of this Agreement shall be finally resolved by arbitration administered by the ICC in accordance with the ICC Rules. The seat of arbitration shall be Tashkent, Uzbekistan. The tribunal shall consist of three arbitrators. This Agreement is governed by Uzbek law.", 1),

    # Optional arbitration / asymmetric clause — only one party has right to arbitrate
    ("Any dispute arising under this Agreement shall be resolved by arbitration administered by the LCIA under the LCIA Rules, provided that only the Lender may elect to submit a dispute to arbitration; the Borrower's exclusive recourse shall be to the courts of England and Wales. The seat of arbitration shall be London.", 1),

    # Arbitration clause in unsigned annex — validity challenge
    ("The parties agree that any disputes arising under this Agreement shall be resolved pursuant to the dispute resolution procedures set out in Annex C hereto, which procedures may include arbitration. The seat of any arbitration shall be determined by the procedures set forth in Annex C.", 1),

    # Time-bar clause that is inconsistent with institutional rules
    ("Any dispute arising under this Agreement shall be submitted to arbitration administered by ICC under the ICC Rules. No claim may be submitted to arbitration more than six months after the claimant became aware, or should have become aware, of the facts giving rise to the claim. The seat shall be Paris. This Agreement is governed by French law.", 1),
    # ============================================================
    # AFA (Association Française d'Arbitrage) — French arbitration
    # Paris is one of the world's leading arbitration seats; AFA is
    # France's primary domestic arbitration institution alongside ICC.
    # ============================================================

    # ---- Healthy: AFA standard clauses (label 0) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the Association Française d'Arbitrage (AFA) in accordance with its Arbitration Rules. The seat of arbitration shall be Paris, France. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement shall be governed by French law.", 0),
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally settled by arbitration administered by the AFA under its Rules of Arbitration. The seat of arbitration shall be Paris, France. The number of arbitrators shall be one. The language of the arbitration shall be French. This Agreement is governed by the laws of France.", 0),
    ("Any dispute arising out of this Agreement shall be referred to and finally resolved by arbitration under the AFA Arbitration Rules. The seat of arbitration shall be Paris. The tribunal shall consist of one arbitrator. This Agreement is governed by French law.", 0),

    # ---- Pathological: AFA defects (label 1) ----
    ("Either party may, at its option, submit any dispute arising under this Agreement to arbitration administered by the AFA under its Arbitration Rules. The seat shall be Paris.", 1),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the Association Française d'Arbitrage in accordance with its Rules. The tribunal shall consist of three arbitrators. This Agreement is governed by French law.", 1),
    ("Any dispute shall be resolved by arbitration administered by the AFA under its Rules. The seat shall be Paris. Notwithstanding the foregoing, either party may bring proceedings before the courts of France. This Agreement is governed by French law.", 1),
    ("Any dispute shall be finally resolved by arbitration administered by the French Arbitration Association under its applicable rules. The seat shall be Paris. This Agreement is governed by French law.", 1),
    ("Any dispute arising out of this Agreement shall be finally settled by arbitration administered by the Association Française d'Arbitrage in accordance with the ICC Rules of Arbitration. The seat shall be Paris. This Agreement is governed by French law.", 1),
    # ============================================================
    # New defect categories — per framework analysis
    # ============================================================

    # ---- Missing language of arbitration (label 1) ----
    # International contracts without language specification create
    # months of procedural dispute and translation cost.
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the ICC in accordance with the ICC Rules of Arbitration. The seat of arbitration shall be Paris. The tribunal shall consist of three arbitrators. This Agreement is governed by French law.", 1),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the LCIA under the LCIA Rules. The seat of arbitration shall be London. There shall be one arbitrator. This Agreement is governed by English law.", 1),
    ("All disputes arising out of this Agreement shall be finally resolved by arbitration administered by HKIAC under the HKIAC Administered Arbitration Rules. The seat shall be Hong Kong. The tribunal shall consist of three arbitrators. This Agreement is governed by Hong Kong law.", 0),

    # ---- Unilateral / asymmetric option clause (label 1) ----
    # One party retains right to litigate while the other is bound to
    # arbitrate. Void or challengeable in several jurisdictions.
    ("Any dispute arising under this Agreement shall be resolved by arbitration administered by the LCIA under the LCIA Rules, provided that only the Lender may elect to submit a dispute to arbitration; the Borrower's exclusive recourse shall be to the courts of England and Wales. The seat of arbitration shall be London. This Agreement is governed by English law.", 1),
    ("Any dispute arising out of this Agreement shall be resolved by arbitration administered by the ICC under the ICC Rules at the option of the Bank only. The Counterparty shall not have the right to initiate arbitration and its sole recourse shall be to the courts of competent jurisdiction. The seat shall be Paris. This Agreement is governed by French law.", 1),
    ("In the event of a dispute, Lender may elect to proceed either by arbitration under the SIAC Rules or by litigation in the courts of Singapore. Borrower's disputes shall be submitted exclusively to arbitration administered by SIAC under the SIAC Rules. The seat shall be Singapore.", 1),

    # ---- Multi-tiered clause without clear trigger mechanism (label 1) ----
    # Pre-arbitration steps (negotiation/mediation) with no defined
    # failure point create a jurisdictional objection on day one.
    ("Any dispute arising out of this Agreement shall first be referred to senior management of both parties for amicable resolution. If the dispute is not resolved, it shall be submitted to arbitration administered by the ICC under the ICC Rules. The seat shall be Paris. This Agreement is governed by French law.", 1),
    ("Any dispute arising under this Agreement shall be subject to mediation prior to arbitration. If mediation fails, the dispute shall be referred to arbitration administered by the LCIA under the LCIA Rules. The seat shall be London. This Agreement is governed by English law.", 1),
    ("In the event of a dispute, the parties shall negotiate in good faith for a period of not less than 60 days before commencing arbitration. Any arbitration shall be administered by SIAC under the SIAC Rules. The seat shall be Singapore. This Agreement is governed by Singapore law.", 1),

    # ---- Unworkable number of arbitrators (label 1) ----
    # Even numbers create deadlock; two-arbitrator clauses are
    # procedurally inoperable under virtually all institutional rules.
    ("Any dispute arising out of this Agreement shall be finally resolved by arbitration administered by the LCIA under the LCIA Rules. The seat shall be London. The parties shall each appoint one arbitrator and the two arbitrators shall jointly render the award. This Agreement is governed by English law.", 1),
    ("Any dispute arising under this Agreement shall be submitted to arbitration administered by the ICC under the ICC Rules. The seat shall be Paris. The tribunal shall consist of two arbitrators, one appointed by each party. This Agreement is governed by French law.", 1),
    ("All disputes shall be finally resolved by arbitration administered by SIAC under the SIAC Rules. The seat shall be Singapore. The arbitral tribunal shall be composed of four arbitrators. This Agreement is governed by Singapore law.", 1),

    # ---- Missing language of arbitration (healthy counterparts, label 0) ----
    # Well-drafted clauses that include language specification
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the ICC in accordance with the ICC Rules of Arbitration. The seat of arbitration shall be Paris. The tribunal shall consist of three arbitrators. The language of arbitration shall be English. This Agreement is governed by French law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the LCIA under the LCIA Rules. The seat of arbitration shall be London. There shall be one arbitrator. The language of arbitration shall be English. This Agreement is governed by English law.", 0),

    # ---- Multi-tiered clause with clear trigger mechanism (healthy, label 0) ----
    ("Any dispute arising out of or in connection with this Agreement shall first be submitted to mediation administered by CEDR. If the dispute is not resolved within 30 days of the commencement of mediation, or such longer period as the parties may agree in writing, the dispute shall be referred to and finally resolved by arbitration administered by the LCIA under the LCIA Rules. The seat of arbitration shall be London. The language of arbitration shall be English. This Agreement is governed by English law.", 0),
    ("Any dispute arising under this Agreement shall first be referred to the chief executive officers of the parties for resolution for a period not exceeding 30 days from the date of written notice of the dispute. Failing resolution within such period, the dispute shall be referred to arbitration administered by the ICC in accordance with the ICC Rules. The seat shall be Singapore. The language shall be English. This Agreement is governed by Singapore law.", 0),
    # ============================================================
    # Expansion batch 3 — additional variants for the five-category
    # framework (structural defects, procedural elements)
    # ============================================================

    # ---- Structural Defects: unilateral option, more real-world variants (label 1) ----
    ("Any dispute arising out of this Agreement shall be finally resolved by arbitration administered by the HKIAC under the HKIAC Administered Arbitration Rules, provided that the Bank alone shall have the right to elect court proceedings in Hong Kong in lieu of arbitration. The seat shall be Hong Kong. The language shall be English. This Agreement is governed by Hong Kong law.", 1),
    ("All disputes shall be referred to arbitration administered by the SIAC under the SIAC Rules, save that the Supplier may at its sole discretion commence proceedings in any court of competent jurisdiction. The seat of arbitration shall be Singapore. This Agreement is governed by Singapore law.", 1),
    ("Any dispute arising under this Agreement shall be resolved exclusively by arbitration administered by the ICC, except that the Licensor reserves the right to seek relief in the courts of New York for any dispute. The seat shall be New York. This Agreement is governed by New York law.", 1),

    # ---- Structural Defects: multi-tier without trigger, more variants (label 1) ----
    ("The parties shall attempt in good faith to resolve any dispute through friendly consultations. If consultations fail, the dispute shall be referred to arbitration administered by CIETAC in accordance with its rules. The seat of arbitration shall be Beijing. This Agreement is governed by Chinese law.", 1),
    ("Any dispute shall first be submitted to mediation under the ICC Mediation Rules. If the mediation is unsuccessful, the dispute shall be finally resolved by arbitration under the ICC Rules of Arbitration. The seat shall be Geneva. This Agreement is governed by Swiss law.", 1),
    ("Prior to initiating arbitration, the parties shall engage in executive-level negotiations. Any unresolved dispute shall then be referred to arbitration administered by the LCIA under the LCIA Rules. The seat shall be London. This Agreement is governed by English law.", 1),

    # ---- Structural Defects: multi-tier WITH clear trigger (healthy, label 0) ----
    ("The parties shall attempt to resolve any dispute through good-faith negotiations for a period of thirty (30) days from written notice of the dispute. Failing resolution within such period, the dispute shall be referred to and finally resolved by arbitration administered by the SIAC in accordance with the SIAC Rules. The seat of arbitration shall be Singapore. The tribunal shall consist of one arbitrator. The language of the arbitration shall be English. This Agreement is governed by Singapore law.", 0),
    ("Any dispute shall first be submitted to mediation administered by the HKIAC. If the dispute is not settled within 45 days of the commencement of the mediation, it shall be referred to and finally resolved by arbitration administered by the HKIAC under the HKIAC Administered Arbitration Rules. The seat of arbitration shall be Hong Kong. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement is governed by Hong Kong law.", 0),

    # ---- Missing Procedural Elements: even-number tribunal, more variants (label 1) ----
    ("Any dispute arising out of this contract shall be finally settled by arbitration administered by the HKIAC under its rules. The seat shall be Hong Kong. Each party shall appoint one arbitrator, and the dispute shall be decided by the two arbitrators so appointed. The language shall be English. This Agreement is governed by Hong Kong law.", 1),
    ("All disputes shall be resolved by arbitration administered by the DIS under the DIS Rules. The seat shall be Frankfurt. The arbitral tribunal shall consist of four arbitrators, two appointed by each party. The language shall be German. This Agreement is governed by German law.", 1),

    # ---- Missing Procedural Elements: language missing in cross-border contract (label 1) ----
    ("Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration administered by the SIAC in accordance with the SIAC Rules. The seat of arbitration shall be Singapore. The tribunal shall consist of three arbitrators. This Agreement is governed by the laws of England and Wales.", 1),
    ("All disputes arising under this international sales contract shall be settled by arbitration administered by the KCAB under its International Arbitration Rules. The seat shall be Seoul. The tribunal shall consist of one arbitrator. This Agreement is governed by Korean law.", 1),

    # ---- Healthy counterparts with full elements (label 0) ----
    ("Any dispute, controversy or claim arising out of or relating to this contract shall be finally resolved by arbitration administered by the KCAB in accordance with its International Arbitration Rules. The seat of arbitration shall be Seoul. The tribunal shall consist of one arbitrator. The language of the arbitration shall be English. This Agreement is governed by Korean law.", 0),
    ("Any dispute arising out of or in connection with this Agreement shall be referred to and finally resolved by arbitration administered by the VIAC under the Vienna Rules. The seat of arbitration shall be Vienna. The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This Agreement is governed by Austrian law.", 0),
]
