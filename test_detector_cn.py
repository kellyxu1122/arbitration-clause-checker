# -*- coding: utf-8 -*-
"""
中文仲裁条款检测引擎单元测试
运行：python3 -m pytest test_detector_cn.py -v
"""

from detector_cn import analyze_clause_cn
from training_data_cn import TRAINING_DATA_CN


def categories(result):
    return {f.category for f in result.flags}


def test_healthy_clause_minimal_flags():
    clause = (
        "因履行本合同所发生的一切争议，应提交中国国际经济贸易仲裁委员会，"
        "按照该会现行有效的仲裁规则进行仲裁。仲裁地为北京。仲裁裁决是终局的，"
        "对双方均有约束力。本合同适用中华人民共和国法律。"
    )
    result = analyze_clause_cn(clause)
    assert categories(result) == set() or categories(result) == {"争议范围表述模糊"}


def test_arbitration_or_litigation_detected():
    clause = "因本合同发生的争议，可以向仲裁委员会申请仲裁，也可以向人民法院起诉。"
    result = analyze_clause_cn(clause)
    assert "或裁或诉" in categories(result)


def test_only_rules_no_institution_detected():
    clause = "因本合同所发生的一切争议，依照国际商会仲裁规则进行仲裁。仲裁地为北京。"
    result = analyze_clause_cn(clause)
    assert "仅约定仲裁规则未约定机构" in categories(result)


def test_conditional_institution_detected():
    clause = (
        "解决合同纠纷的方式：双方友好协商解决，解决不成，"
        "由违约方对方所在地仲裁委员会仲裁。"
    )
    result = analyze_clause_cn(clause)
    assert "条件性约定仲裁机构" in categories(result)


def test_multiple_institutions_detected():
    clause = "因本合同发生的一切争议，提交中国国际经济贸易仲裁委员会或北京仲裁委员会仲裁，仲裁地为北京。"
    result = analyze_clause_cn(clause)
    assert "约定两个以上仲裁机构" in categories(result)


def test_unrecognized_institution_name_detected():
    clause = "因本合同发生的争议，提交环球商事仲裁联合会仲裁解决，仲裁地为上海。"
    result = analyze_clause_cn(clause)
    assert "仲裁机构名称无法识别" in categories(result)


def test_missing_seat_detected():
    clause = (
        "因本合同引起的或与本合同有关的任何争议，均应提交中国国际经济贸易"
        "仲裁委员会，按照该会仲裁规则进行仲裁。仲裁裁决是终局的，对双方均有约束力。"
    )
    result = analyze_clause_cn(clause)
    assert "未约定仲裁地" in categories(result)


def test_rule_engine_accuracy_on_training_set():
    """回归测试：中文规则引擎在标注数据集上的整体准确率不应低于90%。"""
    correct = 0
    for text, true_label in TRAINING_DATA_CN:
        result = analyze_clause_cn(text)
        pred_label = 1 if result.flags else 0
        if pred_label == true_label:
            correct += 1
    accuracy = correct / len(TRAINING_DATA_CN)
    assert accuracy >= 0.90, f"中文规则引擎准确率降至 {accuracy:.1%}"
