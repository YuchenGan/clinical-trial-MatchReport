from clinicaltrials_api import search_trials_basic
from medical_dictionary import (
    CANCER_SYNONYMS, GENE_DRUG_MAPPING, EXCLUDED_CANCER_TYPES,
    PAN_CANCER_KEYWORDS, GENE_FOCUSED_KEYWORDS, TREATMENT_STAGE_SYNONYMS,
    get_cancer_synonyms, get_gene_drugs, is_excluded_cancer,
    is_pan_cancer_trial, is_gene_focused_trial
)
from utils import parse_age, normalize_gender, extract_nct_id
from typing import List, Set, Dict
import asyncio
import re


async def build_initial_trial_pool(user_input) -> list[dict]:
    """
    构建预过滤的初步匹配池 - 只包含真正符合基本条件的试验
    """

    # 1. 构建搜索策略
    search_strategies = build_search_strategies(user_input)

    # 2. 并行执行搜索
    all_trials = []
    search_tasks = []

    for strategy in search_strategies:
        task = search_trials_basic(strategy["query"], strategy.get("max_results"))
        search_tasks.append(task)

    search_results = await asyncio.gather(*search_tasks, return_exceptions=True)

    # 3. 合并去重
    seen_nct_ids = set()
    raw_trials = []

    for result in search_results:
        if isinstance(result, list):
            for trial in result:
                nct_id = extract_nct_id(trial)
                if nct_id and nct_id not in seen_nct_ids:
                    seen_nct_ids.add(nct_id)
                    raw_trials.append(trial)

    # 4. 🚨 关键步骤：硬性预过滤 - 只保留真正符合条件的试验
    eligible_trials = []
    for trial in raw_trials:
        if passes_hard_eligibility_gates(trial, user_input):
            eligible_trials.append(trial)

    print(f"🔍 搜索到 {len(raw_trials)} 个试验，预过滤后剩余 {len(eligible_trials)} 个符合条件的试验")

    return eligible_trials


def passes_hard_eligibility_gates(trial: dict, user_input) -> bool:
    """
    硬性资格门槛检查 - 不符合条件的试验直接排除，不进入评分
    """

    # 提取试验信息
    protocol_section = trial.get("protocolSection", {})
    identification = protocol_section.get("identificationModule", {})
    eligibility = protocol_section.get("eligibilityModule", {})

    title = identification.get("officialTitle", "").lower()
    inclusion_criteria = eligibility.get("inclusionCriteria", "").lower()
    exclusion_criteria = eligibility.get("exclusionCriteria", "").lower()

    # 门槛1: 癌症类型硬性匹配检查
    if not passes_cancer_type_gate(title, inclusion_criteria, user_input):
        return False

    # 门槛2: 年龄硬性限制检查
    if not passes_age_gate(eligibility, user_input):
        return False

    # 门槛3: 性别硬性限制检查
    if not passes_gender_gate(eligibility, user_input):
        return False

    # 门槛4: ECOG硬性限制检查
    if not passes_ecog_gate(inclusion_criteria, exclusion_criteria, user_input):
        return False

    # 门槛5: 严重排除标准检查
    if has_serious_exclusions(exclusion_criteria, user_input):
        return False

    # 门槛6: 只要干预治疗试验，排除观察性研究
    if not is_interventional_trial(trial):
        return False

    return True


def passes_cancer_type_gate(title: str, inclusion: str, user_input) -> bool:
    """
    门槛1: 癌症类型匹配门槛 - 最严格的过滤
    """
    user_cancers = [cancer.lower() for cancer in (user_input.cancer_types or [])]
    user_gene = user_input.gene_mutation.lower() if user_input.gene_mutation else ""

    # 情况1: 试验明确匹配用户的癌症类型
    for user_cancer in user_cancers:
        if user_cancer in title or user_cancer in inclusion:
            return True

    # 情况2: 基因导向试验 - 如果用户有基因突变且试验专注该基因
    if user_gene:
        # 检查试验是否专注该基因突变 - 使用字典
        if is_gene_focused_trial(title, inclusion, user_gene):
            return True

        # 检查是否是泛基因突变试验（针对多种基因突变） - 使用字典
        if any(keyword in title or keyword in inclusion for keyword in GENE_FOCUSED_KEYWORDS):
            # 进一步检查是否包含用户的基因
            if user_gene in inclusion:
                return True

    # 情况3: 泛癌种试验检查 - 使用字典
    if is_pan_cancer_trial(title, inclusion):
        return True

    # 情况4: 严格排除明显不相关的癌症类型 - 使用字典
    for excluded_cancer in EXCLUDED_CANCER_TYPES:
        if excluded_cancer in title:
            # 使用字典检查是否应该排除
            if is_excluded_cancer(excluded_cancer, user_input.cancer_types or []):
                return False

    # 默认情况：如果无法明确分类，保守地包含（后续评分会处理）
    return True


def passes_age_gate(eligibility: dict, user_input) -> bool:
    """
    门槛2: 年龄硬性限制检查
    """
    min_age = eligibility.get("minimumAge", "")
    max_age = eligibility.get("maximumAge", "")

    if not min_age and not max_age:
        return True  # 无年龄限制

    # 解析用户年龄组
    age_ranges = {
        "18-39": (18, 39),
        "40-64": (40, 64),
        "65+": (65, 100)
    }

    user_min, user_max = age_ranges.get(user_input.age_group, (0, 150))

    # 解析试验年龄要求 - 使用utils函数
    trial_min = parse_age(min_age) if min_age else 0
    trial_max = parse_age(max_age) if max_age else 150

    # 检查是否有年龄重叠
    return not (user_max < trial_min or user_min > trial_max)


def passes_gender_gate(eligibility: dict, user_input) -> bool:
    """
    门槛3: 性别硬性限制检查
    """
    trial_gender = eligibility.get("sex", "ALL").upper()

    if trial_gender == "ALL":
        return True

    # 使用utils函数标准化性别
    user_gender_mapped = normalize_gender(user_input.gender)

    return trial_gender in [user_gender_mapped, "ALL"]


def passes_ecog_gate(inclusion: str, exclusion: str, user_input) -> bool:
    """
    门槛4: ECOG硬性限制检查 - 只排除明显不符合的情况
    """
    if not user_input.ecog_score:
        return True  # 没有ECOG信息，保守通过

    user_ecog_num = int(user_input.ecog_score.replace("+", "")) if user_input.ecog_score.replace("+",
                                                                                                 "").isdigit() else 4

    # 查找试验中的ECOG要求
    ecog_patterns = [
        r"ecog.{0,15}[≤<=]\s*([0-3])",
        r"performance.{0,25}status.{0,15}[≤<=]\s*([0-3])",
        r"ecog.{0,15}(\d)\s*or\s*less",
        r"ecog.{0,15}0.{0,5}1"  # "ECOG 0-1"
    ]

    for pattern in ecog_patterns:
        match = re.search(pattern, inclusion, re.IGNORECASE)
        if match:
            try:
                required_max = int(match.group(1))
                if user_ecog_num > required_max:
                    return False  # 明确超出要求，排除
            except (ValueError, IndexError):
                continue

    # 检查排除标准中是否明确排除用户的ECOG
    ecog_exclusion_patterns = [
        rf"ecog.{{0,15}}[≥>=]\s*{user_ecog_num}",
        rf"performance.{{0,25}}status.{{0,15}}[≥>=]\s*{user_ecog_num}"
    ]

    for pattern in ecog_exclusion_patterns:
        if re.search(pattern, exclusion, re.IGNORECASE):
            return False  # 明确被排除

    # ECOG 3+ 的患者对大多数试验过于严格
    if user_ecog_num >= 3:
        # 除非试验明确允许ECOG 3+，否则排除
        if not re.search(r"ecog.{0,15}[≤<=]\s*[3-4]", inclusion, re.IGNORECASE):
            return False

    return True


def has_serious_exclusions(exclusion: str, user_input) -> bool:
    """
    门槛5: 严重排除标准检查
    """
    if not exclusion:
        return False

    # 检查用户的健康状况是否在严重排除标准中
    if user_input.health_conditions:
        serious_conditions = ["cardiac", "renal", "liver", "lung", "brain"]

        for condition in user_input.health_conditions:
            condition_lower = condition.lower()
            for serious in serious_conditions:
                if serious in condition_lower:
                    # 检查是否在排除标准中明确提及
                    exclusion_patterns = [
                        f"severe {serious}",
                        f"active {serious}",
                        f"{serious} failure",
                        f"{serious} disease",
                        f"uncontrolled {serious}"
                    ]

                    for pattern in exclusion_patterns:
                        if pattern in exclusion:
                            return True  # 明确被排除

    # 检查活动性感染
    if user_input.active_infection:
        infection_exclusions = [
            "active infection", "ongoing infection", "uncontrolled infection",
            "systemic infection", "serious infection"
        ]

        if any(ex in exclusion for ex in infection_exclusions):
            return True

    return False


def is_interventional_trial(trial: dict) -> bool:
    """
    门槛6: 干预治疗试验过滤 - 只保留有实际治疗干预的试验
    """
    protocol_section = trial.get("protocolSection", {})

    # 方法1: 检查研究设计类型
    design_info = protocol_section.get("designModule", {})
    study_type = design_info.get("studyType", "").upper()

    # 直接排除观察性研究
    if study_type == "OBSERVATIONAL":
        return False

    # 优先选择干预性研究
    if study_type == "INTERVENTIONAL":
        return True

    # 方法2: 检查是否有干预措施
    arms_info = protocol_section.get("armsInterventionsModule", {})
    interventions = arms_info.get("interventions", [])

    if interventions:
        # 检查干预类型
        for intervention in interventions:
            intervention_type = intervention.get("type", "").lower()

            # 治疗性干预类型
            therapeutic_types = [
                "drug", "biological", "radiation", "procedure",
                "device", "combination product", "genetic"
            ]

            if intervention_type in therapeutic_types:
                return True

    # 方法3: 通过标题关键词判断
    identification = protocol_section.get("identificationModule", {})
    title = identification.get("officialTitle", "").lower()

    # 干预治疗关键词
    intervention_keywords = [
        "phase i", "phase ii", "phase iii", "phase 1", "phase 2", "phase 3",
        "randomized", "controlled", "versus", "vs", "compared",
        "treatment", "therapy", "drug", "medication", "chemotherapy",
        "immunotherapy", "targeted therapy", "radiation", "surgery",
        "combination", "monotherapy", "dose", "efficacy", "safety",
        "clinical trial", "therapeutic"
    ]

    # 观察性研究关键词（需要排除）
    observational_keywords = [
        "observational", "registry", "surveillance", "epidemiologic",
        "natural history", "retrospective", "prospective cohort",
        "case-control", "cross-sectional", "survey", "questionnaire",
        "biomarker study", "correlative", "companion study"
    ]

    # 如果明确是观察性，排除
    if any(keyword in title for keyword in observational_keywords):
        return False

    # 如果有干预性关键词，包含
    if any(keyword in title for keyword in intervention_keywords):
        return True

    # 方法4: 检查主要结局指标
    outcomes_info = protocol_section.get("outcomesModule", {})
    primary_outcomes = outcomes_info.get("primaryOutcomes", [])

    for outcome in primary_outcomes:
        measure = outcome.get("measure", "").lower()

        # 治疗效果相关的主要终点
        therapeutic_endpoints = [
            "response rate", "progression free survival", "overall survival",
            "complete response", "partial response", "disease control",
            "time to progression", "duration of response", "safety",
            "maximum tolerated dose", "dose limiting toxicity", "efficacy"
        ]

        if any(endpoint in measure for endpoint in therapeutic_endpoints):
            return True

    # 方法5: 检查试验阶段
    phases = design_info.get("phases", [])

    # 有明确阶段的通常是干预性试验
    therapeutic_phases = ["PHASE1", "PHASE2", "PHASE3", "PHASE4"]
    if any(phase in phases for phase in therapeutic_phases):
        return True

    # 默认情况：如果无法明确判断，保守地包含
    return True


def build_search_strategies(user_input) -> List[dict]:
    """
    构建更精确的搜索策略 - 避免过于宽泛的搜索
    """
    strategies = []

    cancer_types = user_input.cancer_types or []
    gene_mutation = user_input.gene_mutation
    treatment_stage = user_input.treatment_stage

    # 策略1: 精确组合搜索（最高优先级）
    if gene_mutation and cancer_types:
        for cancer in cancer_types:
            precise_query = f"{gene_mutation} {cancer}"
            strategies.append({
                "query": precise_query,
                "max_results": None,
                "priority": "high"
            })

    # 策略2: 基因主导搜索
    if gene_mutation:
        strategies.extend([
            {
                "query": f"{gene_mutation} mutation",
                "max_results": None,
                "priority": "high"
            },
            {
                "query": f"{gene_mutation} positive",
                "max_results": None,
                "priority": "high"
            },
            {
                "query": f"{gene_mutation} targeted therapy",
                "max_results": None,
                "priority": "medium"
            }
        ])

    # 策略3: 癌症类型精确搜索
    for cancer in cancer_types:
        strategies.append({
            "query": cancer,
            "max_results": None,
            "priority": "medium"
        })

        # 癌症+转移状态组合
        if user_input.metastasis_status:
            strategies.append({
                "query": f"{cancer} {user_input.metastasis_status}",
                "max_results": None,
                "priority": "medium"
            })

    # 策略4: 扩展搜索（但更精确）
    expanded_queries = expand_search_terms_precise(cancer_types, gene_mutation)
    for expanded_query in expanded_queries:
        strategies.append({
            "query": expanded_query,
            "max_results": None,
            "priority": "low"
        })

    return strategies


def expand_search_terms_precise(cancer_types: List[str], gene_mutation: str = None) -> List[str]:
    """
    More precise search term expansion using medical dictionary
    """
    expanded_terms = []

    # Expand cancer type synonyms using dictionary
    for cancer in cancer_types:
        synonyms = get_cancer_synonyms(cancer)
        expanded_terms.extend(synonyms[:3])  # Limit to 3 per cancer type

    # Expand gene-related drug terms using dictionary
    if gene_mutation:
        drugs = get_gene_drugs(gene_mutation)
        expanded_terms.extend(drugs[:3])  # Limit to 3 drugs per gene

    return expanded_terms[:8]  # Control total number