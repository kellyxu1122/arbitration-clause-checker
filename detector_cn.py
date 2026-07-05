# -*- coding: utf-8 -*-
"""
中国仲裁条款瑕疵检测引擎（Chinese Arbitration Clause Pathology Detector）
================================================================
本模块独立于英文检测引擎(detector.py)设计，规则依据中国仲裁法及
《最高人民法院关于适用〈中华人民共和国仲裁法〉若干问题的解释》
(法释〔2006〕7号，简称"仲裁法司法解释")相关条文，并结合公开检索到的
法院典型案例归纳。

核心法律依据：
  - 仲裁法司法解释第3条：仲裁机构名称不准确，但能确定具体仲裁机构的，
    应认定选定了仲裁机构（即：名称瑕疵不必然无效，需结合上下文判断）
  - 仲裁法司法解释第4条：仅约定仲裁规则、未约定仲裁机构的，视为
    未约定仲裁机构（但能通过规则推导出唯一机构的除外）
  - 仲裁法司法解释第5条：约定两个以上仲裁机构，且双方未能就选择
    达成一致的，仲裁协议无效
  - 仲裁法司法解释第6条：约定"由某地仲裁机构仲裁"，该地有两个以上
    仲裁机构且双方未能达成一致选择的，无效；尤其是"违约方/守约方
    所在地仲裁委员会"这类条件性约定，因仲裁前无法确定具体机构，
    实践中常被认定为约定不明而无效
  - 仲裁法司法解释第7条：约定"或裁或诉"（既可申请仲裁也可向法院
    起诉）的，仲裁协议无效——这是与英文规则中"conflicting mechanisms"
    类似但后果更严格的中国特有规则：英美法系下"或裁或诉"条款通常被
    认定为存在歧义需要法院解释，而中国法下直接规定无效

本引擎与英文引擎(detector.py)是两套独立的规则体系，刻意没有做逐条
"翻译"，因为两大法系对同一类瑕疵的法律后果并不相同（参见上面第7条
与英文 check_multi_tier_conflict 的对比），翻译规则会掩盖这一实质性
法律差异。
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class FlagCN:
    category: str
    severity: str          # "high" | "medium" | "low"
    message: str
    matched_text: str = ""


@dataclass
class AnalysisResultCN:
    clause: str
    flags: List[FlagCN] = field(default_factory=list)

    @property
    def risk_score(self) -> int:
        weights = {"high": 3, "medium": 2, "low": 1}
        return sum(weights[f.severity] for f in self.flags)

    @property
    def risk_level(self) -> str:
        score = self.risk_score
        if score == 0:
            return "低风险"
        elif score <= 3:
            return "中等风险"
        else:
            return "高风险"


# ---------------------------------------------------------------------------
# 已知中国及常见涉外仲裁机构名称库（用于检测机构名称是否可识别）
# ---------------------------------------------------------------------------
KNOWN_INSTITUTIONS_CN = [
    # 国家级/重点机构
    "中国国际经济贸易仲裁委员会", "贸仲", "贸仲委", "cietac",
    "中国国际经济贸易仲裁委员会上海分会", "中国国际经济贸易仲裁委员会华南分会",
    "中国国际经济贸易仲裁委员会南中国海仲裁中心", "中国国际经济贸易仲裁委员会西南分会",
    "北京仲裁委员会", "北京国际仲裁中心", "北仲",
    "上海国际仲裁中心", "上海国际经济贸易仲裁委员会", "上海仲裁委员会",
    "深圳国际仲裁院", "华南国际经济贸易仲裁委员会", "深国仲",
    "广州仲裁委员会", "广仲",
    "海南国际仲裁院", "海仲",
    "中国海事仲裁委员会", "海仲委",
    # 涉外常用机构
    "香港国际仲裁中心", "hkiac",
    "新加坡国际仲裁中心", "siac",
    "国际商会", "国际商会仲裁院", "icc",
    "伦敦国际仲裁院", "lcia",
    # 二三线城市仲裁委员会（中国仲裁协会成员机构）
    "武汉仲裁委员会", "武汉",
    "成都仲裁委员会", "成都",
    "西安仲裁委员会", "西安",
    "杭州仲裁委员会", "杭州",
    "南京仲裁委员会", "南京",
    "重庆仲裁委员会", "重庆",
    "天津仲裁委员会", "天津",
    "济南仲裁委员会", "济南",
    "郑州仲裁委员会", "郑州",
    "长沙仲裁委员会", "长沙",
    "沈阳仲裁委员会", "沈阳",
    "宁波仲裁委员会", "宁波",
    "青岛仲裁委员会", "青岛",
    "苏州仲裁委员会", "苏州",
    "厦门仲裁委员会", "厦门",
    "福州仲裁委员会", "福州",
    "合肥仲裁委员会", "合肥",
    "石家庄仲裁委员会", "石家庄",
    "南昌仲裁委员会", "南昌",
    "哈尔滨仲裁委员会", "哈尔滨",
    "长春仲裁委员会", "长春",
    "太原仲裁委员会", "太原",
    "南宁仲裁委员会", "南宁",
    "贵阳仲裁委员会", "贵阳",
    "昆明仲裁委员会", "昆明",
    "乌鲁木齐仲裁委员会", "乌鲁木齐",
    "兰州仲裁委员会", "兰州",
    "银川仲裁委员会", "银川",
    "西宁仲裁委员会", "西宁",
    "呼和浩特仲裁委员会", "呼和浩特",
    "拉萨仲裁委员会", "拉萨",
    "海口仲裁委员会", "海口",
    "无锡仲裁委员会", "无锡",
    "大连仲裁委员会", "大连",
    "温州仲裁委员会", "温州",
    "东莞仲裁委员会", "东莞",
    "珠海仲裁委员会", "珠海",
    "佛山仲裁委员会", "佛山",
]

# 中国大陆主要城市及该地是否存在多家仲裁机构的简化映射
# （用于检测"某地仲裁委员会"这类约定是否可能因当地存在多家机构而不明确）
MULTI_INSTITUTION_CITIES = {
    "北京": ["北京仲裁委员会", "中国国际经济贸易仲裁委员会"],
    "上海": ["上海仲裁委员会", "上海国际经济贸易仲裁委员会", "上海国际仲裁中心"],
    "深圳": ["深圳国际仲裁院", "深圳仲裁委员会"],
}


def _find_all(pattern, text, flags=0):
    return list(re.finditer(pattern, text, flags))


def check_arbitration_litigation_both(text: str) -> List[FlagCN]:
    """对应司法解释第7条：约定"或裁或诉"——既可仲裁又可诉讼，无效。
    这是中国法下后果最严重的一类瑕疵：不同于很多英美法域将类似表述
    解释为"存在歧义、需进一步解释"，中国法直接规定此类条款无效。"""
    flags = []
    has_arbitration = re.search(r"仲裁", text)
    if not has_arbitration:
        return flags

    # 常见"或裁或诉"表述模式——按真实合同措辞归纳
    patterns = [
        # 先仲裁后诉讼（标准写法，允许机构名带城市前缀如"北京仲裁委员会"）
        r"(可以|可)向?[^。，]{0,12}(仲裁机构|仲裁委员会)?申请仲裁.{0,20}也可(以)?向(人民法院|法院)起诉",
        # 先诉讼后仲裁
        r"(可以|可)向(人民法院|法院)起诉.{0,20}也可(以)?(向仲裁机构|向仲裁委员会|申请)?仲裁",
        # 既可…也可…（双向 + 提交仲裁机构变体）
        r"既可(以)?(提交)?[^。，]{0,10}仲裁.{0,15}也可(以)?(向.{0,10})?(诉讼|起诉)",
        r"既可(以)?(诉讼|起诉).{0,15}也可(以)?仲裁",
        # "仲裁或诉讼"/"诉讼或仲裁"直接并列
        r"仲裁或(者)?(诉讼|起诉|向.{0,6}法院)",
        r"(诉讼|起诉|向.{0,6}法院)或(者)?仲裁",
        # 申请仲裁或向法院起诉
        r"申请仲裁或(者)?向.{0,15}(人民法院|法院)起诉",
        # "交由法院或仲裁委"/"交由仲裁委或法院"句式（真实合同常见）
        r"(交由|提交|交).{0,10}(人民法院|法院).{0,5}或.{0,15}(仲裁委|仲裁院|仲裁机构|仲裁中心)",
        r"(交由|提交|交).{0,10}(仲裁委|仲裁院|仲裁机构|仲裁中心).{0,5}或.{0,15}(人民法院|法院)",
        # "或向法院起诉"附加在仲裁条款后
        r"仲裁.{0,30}或(者)?(向.{0,6})?(人民法院|法院)(起诉|提起诉讼|管辖)",
        # "守约方可向…仲裁或向…法院提起诉讼"（真实判例措辞）
        r"(仲裁|仲裁委|仲裁院).{0,10}或(者)?.{0,10}(人民法院|法院).{0,10}(起诉|诉讼|提起)",
        # "亦可向…人民法院提起诉讼/起诉"——"亦可"变体（真实合同高频）
        r"仲裁.{0,25}亦可(以)?向?[^。]{0,20}(人民法院|法院)(提起诉讼|起诉)",
        # "亦可以诉讼方式解决"
        r"仲裁.{0,25}亦可(以)?(以)?诉讼(方式)?(解决)?",
        # "也可向…法院起诉"——不带"申请仲裁"动词的前半句（如"可提交X仲裁委仲裁，也可向Y法院起诉"）
        r"仲裁.{0,30}也可(以)?向[^。]{0,20}(人民法院|法院)起诉",
        # "亦可由…提起诉讼"
        r"仲裁.{0,25}亦可(以)?由[^。]{0,15}提起诉讼",
        # "保留向法院起诉的权利"——仲裁条款附加诉权保留
        r"仲裁.{0,40}保留向?(人民法院|法院)?(提起诉讼|起诉)(的权利)?",
        # "同时同意…法院…管辖"——仲裁与法院管辖并存约定
        r"仲裁.{0,40}同时同意[^。]{0,15}(人民法院|法院)[^。]{0,10}管辖",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            flags.append(FlagCN(
                category="或裁或诉",
                severity="high",
                message=(
                    "条款同时约定了仲裁与诉讼两种争议解决方式（'或裁或诉'）。"
                    "根据《最高人民法院关于适用〈中华人民共和国仲裁法〉若干问题"
                    "的解释》第七条，当事人约定争议可以向仲裁机构申请仲裁也可以"
                    "向人民法院起诉的，仲裁协议无效（除非一方已申请仲裁、对方在"
                    "法定异议期间内未提出异议）。这是中国法下后果最严重的条款瑕疵"
                    "之一，与许多英美法域将类似表述解释为'存在歧义'不同，中国法"
                    "直接认定此类条款无效。"
                ),
                matched_text=m.group(0),
            ))
            break  # 同一类问题只报一次
    return flags


def check_only_rules_no_institution(text: str) -> List[FlagCN]:
    """对应司法解释第4条：仅约定仲裁规则，未约定仲裁机构的，视为
    未约定仲裁机构（除非按约定规则能推导出唯一机构）。

    注意：以下表述不属于此类瑕疵，应豁免：
    - "提交XX仲裁委员会，按照该会仲裁规则"——"该会"是对前文机构的回指
    - "提交XX仲裁委员会，依照该会现行有效的仲裁规则"——同上
    这类表述已明确约定了机构，"该会规则"仅是对规则来源的说明。
    """
    flags = []
    has_arbitration = re.search(r"仲裁", text)
    if not has_arbitration:
        return flags

    # 豁免1：含"该会仲裁规则"/"该院仲裁规则"等回指表述，说明已约定了机构
    has_pronoun_reference = re.search(r"该(会|院|中心|委员会)(现行有效的)?仲裁规则", text)
    if has_pronoun_reference:
        return flags

    # 豁免2：检测是否提及"提交/由XX机构管理"这种明确指定管理机构的表述
    # 扩展为匹配"仲裁委员会"结尾的任意机构名，不仅限于已知机构列表
    has_administering_institution = re.search(
        r"(提交|提请|由)[^。，,]{0,15}"
        r"(仲裁委员会|仲裁院|仲裁中心|仲裁庭)"
        r"[^。]{0,15}(仲裁|管理|受理|按照|依照)",
        text,
    )
    if has_administering_institution:
        return flags

    # 检测是否仅提及"规则"而无明确管理机构
    mentions_rules_only = re.search(r"(根据|依照|按照|适用).{0,20}仲裁规则", text)
    if mentions_rules_only:
        flags.append(FlagCN(
            category="仅约定仲裁规则未约定机构",
            severity="high",
            message=(
                "条款仅约定了适用的仲裁规则（'%s'），但未明确约定由具体哪家"
                "仲裁机构管理仲裁。根据仲裁法司法解释第四条，仲裁协议仅约定"
                "纠纷适用的仲裁规则的，视为未约定仲裁机构，但当事人达成补充"
                "协议或者按照约定的仲裁规则能够确定仲裁机构的除外。例如仅"
                "约定'依照国际商会仲裁规则仲裁'而未写明'提交国际商会仲裁院"
                "管理仲裁'，该条款可能被认定无效（参见相关法院判例，当事人"
                "仅约定适用《国际商会仲裁规则》而未约定仲裁机构的，仲裁条款"
                "被认定无效）。" % mentions_rules_only.group(0)
            ),
            matched_text=mentions_rules_only.group(0),
        ))
    return flags


def check_vague_institution_by_location(text: str) -> List[FlagCN]:
    """对应司法解释第6条：约定"由某地仲裁机构仲裁"，该地有两个以上
    仲裁机构且双方未能达成一致的，无效。重点检测两类高风险表述：
    1. 条件性表述（"违约方所在地""守约方所在地"）——仲裁前无法确定具体地点
    2. 提及多机构城市但未指明具体机构名称
    """
    flags = []
    # 条件性表述：违约方/守约方所在地仲裁委员会
    conditional_pattern = re.search(
        r"(违约方|守约方|被告|原告|对方)(所在地|住所地)?.{0,6}(当地)?仲裁(委员会|机构)",
        text,
    )
    if conditional_pattern:
        flags.append(FlagCN(
            category="条件性约定仲裁机构",
            severity="high",
            message=(
                "条款约定以'%s'作为确定仲裁机构的依据。此类条件性约定因在"
                "纠纷发生、实体审理之前无法确定哪一方构成'违约方'或'守约方'，"
                "导致具体仲裁机构在订立合同时及仲裁启动前均无法确定。多地法院"
                "（如(2020)鲁03民特207号、(2016)甘05民特1号等案例）已将此类"
                "约定认定为仲裁机构约定不明确，仲裁条款无效。"
                % conditional_pattern.group(0)
            ),
            matched_text=conditional_pattern.group(0),
        ))

    # 提及多机构城市但未指明具体机构
    for city, institutions in MULTI_INSTITUTION_CITIES.items():
        city_only_pattern = re.search(
            r"由%s(市)?(的)?仲裁(委员会|机构)(仲裁|解决|管辖)" % city, text
        )
        has_specific_institution = any(inst in text for inst in institutions)
        if city_only_pattern and not has_specific_institution:
            flags.append(FlagCN(
                category="地名+仲裁机构表述不明确",
                severity="medium",
                message=(
                    "条款约定由'%s'的仲裁机构管辖，但%s存在多家仲裁机构（如%s），"
                    "且条款未指明具体机构名称。根据仲裁法司法解释第六条，该地有"
                    "两个以上仲裁机构的，当事人需协议选择其中之一，否则可能因"
                    "约定不明确导致仲裁协议无效。"
                    % (city, city, "、".join(institutions[:2]))
                ),
                matched_text=city_only_pattern.group(0),
            ))
    return flags


def check_multiple_institutions(text: str) -> List[FlagCN]:
    """对应司法解释第5条：约定两个以上仲裁机构，且当事人不能就选择
    达成一致的，仲裁协议无效。"""
    flags = []
    mentioned = [inst for inst in KNOWN_INSTITUTIONS_CN if inst in text]
    # 去重同一机构的不同别名（简单按机构全称分组，避免"贸仲"和"中国国际经济贸易仲裁委员会"被算作两个不同机构）
    canonical_groups = {
        "贸仲": ["中国国际经济贸易仲裁委员会", "贸仲", "贸仲委", "cietac"],
        "北仲": ["北京仲裁委员会", "北京国际仲裁中心", "北仲"],
        "上仲": ["上海仲裁委员会"],
        "上国仲": ["上海国际经济贸易仲裁委员会", "上海国际仲裁中心"],
        "深国仲": ["深圳国际仲裁院", "华南国际经济贸易仲裁委员会", "深国仲"],
        "广仲": ["广州仲裁委员会", "广仲"],
        "海仲院": ["海南国际仲裁院", "海仲"],
        "hkiac": ["香港国际仲裁中心", "hkiac"],
        "siac": ["新加坡国际仲裁中心", "siac"],
        "icc": ["国际商会", "国际商会仲裁院", "icc"],
        "lcia": ["伦敦国际仲裁院", "lcia"],
    }
    distinct_institutions = set()
    for canonical, aliases in canonical_groups.items():
        if any(a in text for a in aliases):
            distinct_institutions.add(canonical)

    if len(distinct_institutions) >= 2:
        has_selection_mechanism = re.search(
            r"(协议选择|由申请人选择|由提起仲裁一方选择|任择其一)", text
        )
        if not has_selection_mechanism:
            flags.append(FlagCN(
                category="约定两个以上仲裁机构",
                severity="high",
                message=(
                    "条款中出现了%d个不同的仲裁机构（%s），且未约定明确的选择"
                    "机制。根据仲裁法司法解释第五条，仲裁协议约定两个以上仲裁"
                    "机构的，当事人可以协议选择其中一个申请仲裁；当事人不能就"
                    "仲裁机构选择达成一致的，仲裁协议无效。"
                    % (len(distinct_institutions), "、".join(distinct_institutions))
                ),
            ))
    return flags


def check_institution_name_typo(text: str) -> List[FlagCN]:
    """对应司法解释第3条：机构名称不准确但能确定具体机构的，仍认定
    选定了仲裁机构（这是一条"容错"规则）。本检测的目的不是简单判断
    "名称是否完全匹配"，而是识别名称偏离已知机构名称较大、可能导致
    无法确定具体机构的情形（区别于轻微的简称/笔误）。

    注意：符合"[城市名]+仲裁委员会"格式的表述一律视为合法
    （中国200多家仲裁机构绝大多数以城市命名），仅对包含虚构机构类型
    名称（如"仲裁联合会""仲裁总会"）的情形报警。
    """
    flags = []
    # 查找形如"XX仲裁委员会/中心/院"等的表述
    candidates = _find_all(
        r"([\u4e00-\u9fa5]{2,20}(仲裁委员会|仲裁中心|仲裁院|仲裁庭|仲裁局|仲裁联合会|仲裁协会|仲裁总会|仲裁机构))", text
    )
    # 跳过"当地/对方/守约方/违约方所在地仲裁委员会"这类条件性/泛指表述
    skip_prefixes = ("当地", "对方", "守约方", "违约方", "原告", "被告")
    # 合法后缀：带这些后缀的标准机构名不触发告警
    standard_suffixes = ("仲裁委员会", "仲裁中心", "仲裁院")
    # 可疑后缀：这些后缀不是正式机构类型，高度可能是虚构机构
    suspicious_suffixes = ("仲裁联合会", "仲裁协会", "仲裁总会", "仲裁局")

    for m in candidates:
        name = m.group(1)
        suffix = m.group(2)

        if any(name.startswith(p) for p in skip_prefixes) or "当地" in name:
            continue

        # 可疑后缀直接报警（这类机构类型在中国官方认可机构中不存在）
        if suffix in suspicious_suffixes:
            flags.append(FlagCN(
                category="仲裁机构名称无法识别",
                severity="medium",
                message=(
                    "条款中提及的'%s'所用机构类型名称（'%s'）不属于中国法定"
                    "仲裁机构类型。中国法定仲裁机构名称通常以'仲裁委员会'、"
                    "'仲裁中心'或'仲裁院'结尾，经国务院有关主管部门或省、"
                    "自治区、直辖市人民政府登记注册。建议核实该机构是否为"
                    "依法登记的仲裁机构，否则仲裁条款存在无效风险。" % (name, suffix)
                ),
                matched_text=name,
            ))
            continue

        # 标准后缀：检查名称是否在已知机构库中可识别
        recognized = any(
            name in known or known in name or _name_overlap(name, known) >= 0.5
            for known in KNOWN_INSTITUTIONS_CN
            if any(s in known for s in standard_suffixes)
        )
        # 额外豁免：符合"XX仲裁委员会"标准格式（城市名+仲裁委员会）
        # 中国所有正式仲裁机构均可以此格式命名，不要求逐一列举
        if not recognized and suffix == "仲裁委员会":
            recognized = True  # 按司法解释第3条容错原则，能确定城市即视为可识别

        if not recognized:
            flags.append(FlagCN(
                category="仲裁机构名称无法识别",
                severity="medium",
                message=(
                    "条款中提及的'%s'未能匹配任何已知仲裁机构名称。根据仲裁法"
                    "司法解释第三条，名称不准确但能确定具体仲裁机构的，仍视为"
                    "选定了该机构；但若名称偏差过大导致无法确定具体指向哪一"
                    "机构，仲裁条款存在被认定无效的风险。建议核实该机构的"
                    "准确法定名称。" % name
                ),
                matched_text=name,
            ))
    return flags


def _name_overlap(a: str, b: str) -> float:
    """简单的字符重叠率计算，用于辅助判断机构名称是否大致匹配。"""
    set_a, set_b = set(a), set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def check_missing_seat_or_language(text: str) -> List[FlagCN]:
    """涉外仲裁中，仲裁地（影响程序法适用）和仲裁语言常被忽略，
    尤其在中国企业自行起草的英文/双语合同中较为常见。"""
    flags = []
    has_arbitration = re.search(r"仲裁", text)
    has_seat = re.search(
        r"(仲裁地(点)?(为|是|应为|应在|设在))|(在[\u4e00-\u9fa5]{2,8}(进行)?仲裁)|(仲裁地点在)",
        text,
    )
    if has_arbitration and not has_seat:
        flags.append(FlagCN(
            category="未约定仲裁地",
            severity="medium",
            message=(
                "条款未明确约定仲裁地。仲裁地决定了仲裁程序法的适用以及"
                "法院对仲裁的监督管辖权归属，在涉外仲裁中尤为重要（仲裁地"
                "与开庭地、机构所在地可以不同）。建议明确约定，例如"
                "'仲裁地为北京'。"
            ),
        ))
    return flags


def check_scope_ambiguity(text: str) -> List[FlagCN]:
    """检测争议解决范围是否使用了标准的概括性表述。范围过窄或表述
    模糊可能导致部分争议被认定不属于仲裁协议约定范围。"""
    flags = []
    broad_scope = re.search(
        r"(因|与|凡因)([\u4e00-\u9fa5]{0,4})?(本合同|本协议)[^。]{0,25}(引起|发生|产生)(的)?[^。]{0,15}(一切|任何|所有)(争议|纠纷)",
        text,
    )
    if not broad_scope:
        flags.append(FlagCN(
            category="争议范围表述模糊",
            severity="low",
            message=(
                "条款未使用标准的概括性范围表述（如'因本合同发生的一切"
                "争议'）。范围表述过窄或模糊，可能导致一方主张特定争议"
                "不在仲裁协议约定范围内，从而引发管辖权异议。"
            ),
        ))
    return flags


ALL_CHECKS_CN = [
    check_arbitration_litigation_both,
    check_only_rules_no_institution,
    check_vague_institution_by_location,
    check_multiple_institutions,
    check_institution_name_typo,
    check_missing_seat_or_language,
    check_scope_ambiguity,
]


def analyze_clause_cn(text: str) -> AnalysisResultCN:
    """对中文仲裁条款运行全部检测规则，返回结构化结果。"""
    result = AnalysisResultCN(clause=text)
    for check in ALL_CHECKS_CN:
        result.flags.extend(check(text))
    return result
