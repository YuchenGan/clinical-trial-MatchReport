"""
Medical Dictionary for Clinical Trial Matching
Contains comprehensive mappings of cancer types, gene mutations, and drug relationships
"""

# Cancer Type Synonyms and Related Terms
CANCER_SYNONYMS = {
    # Lung Cancer
    "lung cancer": [
        "NSCLC", "non-small cell lung cancer", "small cell lung cancer", "SCLC",
        "pulmonary carcinoma", "bronchogenic carcinoma", "pulmonary neoplasm",
        "lung adenocarcinoma", "lung squamous cell carcinoma", "large cell lung cancer"
    ],

    # Breast Cancer
    "breast cancer": [
        "mammary carcinoma", "ductal carcinoma", "lobular carcinoma",
        "triple negative breast cancer", "TNBC", "HER2 positive breast cancer",
        "hormone receptor positive breast cancer", "invasive ductal carcinoma",
        "invasive lobular carcinoma", "inflammatory breast cancer"
    ],

    # Colorectal Cancer
    "colon cancer": [
        "colorectal cancer", "CRC", "rectal cancer", "bowel cancer",
        "adenocarcinoma of colon", "sigmoid colon cancer", "cecal cancer"
    ],
    "colorectal cancer": [
        "colon cancer", "rectal cancer", "CRC", "bowel cancer",
        "colorectal adenocarcinoma", "colorectal carcinoma"
    ],

    # Liver Cancer
    "liver cancer": [
        "hepatocellular carcinoma", "HCC", "hepatic carcinoma",
        "primary liver cancer", "hepatoma", "liver cell carcinoma"
    ],

    # Kidney Cancer
    "kidney cancer": [
        "renal cell carcinoma", "RCC", "renal carcinoma", "nephrocarcinoma",
        "clear cell renal cell carcinoma", "papillary renal cell carcinoma"
    ],

    # Stomach Cancer
    "stomach cancer": [
        "gastric cancer", "gastric carcinoma", "gastric adenocarcinoma",
        "gastroesophageal junction cancer", "GEJ cancer"
    ],

    # Pancreatic Cancer
    "pancreatic cancer": [
        "pancreas cancer", "pancreatic adenocarcinoma", "PDAC",
        "pancreatic ductal adenocarcinoma", "pancreatic neuroendocrine tumor", "PNET"
    ],

    # Prostate Cancer
    "prostate cancer": [
        "prostatic carcinoma", "prostate adenocarcinoma", "PCa",
        "castration resistant prostate cancer", "CRPC", "metastatic prostate cancer"
    ],

    # Ovarian Cancer
    "ovarian cancer": [
        "ovary cancer", "ovarian carcinoma", "epithelial ovarian cancer",
        "serous ovarian cancer", "mucinous ovarian cancer", "ovarian adenocarcinoma"
    ],

    # Bladder Cancer
    "bladder cancer": [
        "urothelial carcinoma", "transitional cell carcinoma", "TCC",
        "bladder carcinoma", "muscle invasive bladder cancer", "MIBC",
        "non-muscle invasive bladder cancer", "NMIBC"
    ],

    # Head and Neck Cancer
    "head and neck cancer": [
        "HNSCC", "head and neck squamous cell carcinoma", "oral cancer",
        "laryngeal cancer", "pharyngeal cancer", "nasopharyngeal cancer",
        "oropharyngeal cancer", "hypopharyngeal cancer"
    ],

    # Brain Cancer
    "brain cancer": [
        "glioblastoma", "GBM", "glioma", "brain tumor", "CNS tumor",
        "astrocytoma", "oligodendroglioma", "meningioma", "brain metastases"
    ],

    # Blood Cancers
    "leukemia": [
        "acute myeloid leukemia", "AML", "acute lymphoblastic leukemia", "ALL",
        "chronic myeloid leukemia", "CML", "chronic lymphocytic leukemia", "CLL",
        "acute promyelocytic leukemia", "APL", "hairy cell leukemia"
    ],

    "lymphoma": [
        "hodgkin lymphoma", "non-hodgkin lymphoma", "NHL", "B-cell lymphoma",
        "T-cell lymphoma", "diffuse large B-cell lymphoma", "DLBCL",
        "follicular lymphoma", "mantle cell lymphoma", "marginal zone lymphoma"
    ],

    "myeloma": [
        "multiple myeloma", "MM", "plasma cell myeloma", "plasmacytoma",
        "light chain myeloma", "non-secretory myeloma"
    ],

    # Sarcoma
    "sarcoma": [
        "soft tissue sarcoma", "bone sarcoma", "osteosarcoma", "liposarcoma",
        "leiomyosarcoma", "rhabdomyosarcoma", "synovial sarcoma", "fibrosarcoma",
        "angiosarcoma", "chondrosarcoma", "Ewing sarcoma", "GIST"
    ],

    # Skin Cancer
    "melanoma": [
        "malignant melanoma", "cutaneous melanoma", "mucosal melanoma",
        "ocular melanoma", "uveal melanoma", "acral melanoma"
    ],

    # Other Cancers
    "thyroid cancer": [
        "papillary thyroid cancer", "follicular thyroid cancer", "medullary thyroid cancer",
        "anaplastic thyroid cancer", "differentiated thyroid cancer"
    ],

    "esophageal cancer": [
        "esophagus cancer", "esophageal adenocarcinoma", "esophageal squamous cell carcinoma",
        "gastroesophageal junction cancer", "Barrett's adenocarcinoma"
    ],

    "cervical cancer": [
        "cervix cancer", "cervical carcinoma", "cervical squamous cell carcinoma",
        "cervical adenocarcinoma", "HPV-related cervical cancer"
    ],

    "endometrial cancer": [
        "uterine cancer", "endometrial carcinoma", "uterine corpus cancer",
        "endometrioid adenocarcinoma", "serous endometrial cancer"
    ]
}

# Gene Mutations and Associated Targeted Therapies
GENE_DRUG_MAPPING = {
    # EGFR Pathway
    "EGFR": [
        "osimertinib", "gefitinib", "erlotinib", "afatinib", "dacomitinib",
        "necitumumab", "cetuximab", "panitumumab", "amivantamab"
    ],

    # ALK Pathway
    "ALK": [
        "crizotinib", "alectinib", "ceritinib", "brigatinib", "lorlatinib"
    ],

    # BRAF Pathway
    "BRAF": [
        "vemurafenib", "dabrafenib", "trametinib", "cobimetinib",
        "encorafenib", "binimetinib"
    ],

    # HER2 Pathway
    "HER2": [
        "trastuzumab", "pertuzumab", "T-DM1", "trastuzumab emtansine",
        "lapatinib", "neratinib", "tucatinib", "margetuximab", "fam-trastuzumab deruxtecan"
    ],

    # KRAS Pathway
    "KRAS": [
        "sotorasib", "adagrasib", "KRAS G12C inhibitor", "AMG 510", "MRTX849"
    ],

    # ROS1 Pathway
    "ROS1": [
        "crizotinib", "ceritinib", "lorlatinib", "entrectinib", "repotrectinib"
    ],

    # MET Pathway
    "MET": [
        "crizotinib", "cabozantinib", "tepotinib", "capmatinib", "savolitinib"
    ],

    # RET Pathway
    "RET": [
        "selpercatinib", "pralsetinib", "vandetanib", "cabozantinib"
    ],

    # NTRK Pathway
    "NTRK": [
        "larotrectinib", "entrectinib"
    ],
    "TRK": [
        "larotrectinib", "entrectinib"
    ],

    # PI3K/AKT/mTOR Pathway
    "PIK3CA": [
        "alpelisib", "inavolisib", "capivasertib", "ipatasertib"
    ],
    "AKT": [
        "capivasertib", "ipatasertib"
    ],
    "MTOR": [
        "everolimus", "temsirolimus"
    ],

    # DNA Repair Pathway
    "BRCA1": [
        "olaparib", "rucaparib", "niraparib", "talazoparib", "PARP inhibitor",
        "veliparib", "pamiparib"
    ],
    "BRCA2": [
        "olaparib", "rucaparib", "niraparib", "talazoparib", "PARP inhibitor",
        "veliparib", "pamiparib"
    ],
    "ATM": [
        "olaparib", "PARP inhibitor"
    ],

    # Immune Checkpoint Pathway
    "PD-L1": [
        "pembrolizumab", "nivolumab", "atezolizumab", "durvalumab", "avelumab",
        "cemiplimab", "dostarlimab"
    ],
    "PD-1": [
        "pembrolizumab", "nivolumab", "cemiplimab", "dostarlimab", "retifanlimab"
    ],
    "CTLA-4": [
        "ipilimumab", "tremelimumab"
    ],

    # Metabolic Pathway
    "IDH1": [
        "ivosidenib", "olutasidenib"
    ],
    "IDH2": [
        "enasidenib"
    ],

    # Kinase Pathway
    "FLT3": [
        "midostaurin", "gilteritinib", "sorafenib", "quizartinib"
    ],
    "JAK2": [
        "ruxolitinib", "fedratinib", "pacritinib"
    ],
    "BTK": [
        "ibrutinib", "acalabrutinib", "zanubrutinib"
    ],

    # FGFR Pathway
    "FGFR": [
        "erdafitinib", "pemigatinib", "infigratinib", "futibatinib"
    ],
    "FGFR1": [
        "erdafitinib", "pemigatinib", "infigratinib"
    ],
    "FGFR2": [
        "pemigatinib", "infigratinib", "futibatinib"
    ],
    "FGFR3": [
        "erdafitinib", "pemigatinib"
    ],

    # Cell Cycle Pathway
    "CDK4": [
        "palbociclib", "ribociclib", "abemaciclib"
    ],
    "CDK6": [
        "palbociclib", "ribociclib", "abemaciclib"
    ],

    # Angiogenesis Pathway
    "VEGF": [
        "bevacizumab", "ramucirumab", "aflibercept"
    ],
    "VEGFR": [
        "sunitinib", "sorafenib", "pazopanib", "axitinib", "cabozantinib"
    ],

    # Tumor Suppressor Genes
    "TP53": [
        "APR-246", "PRIMA-1"
    ],
    "RB1": [
        "CDK4/6 inhibitor"
    ],

    # Fusion Genes
    "BCR-ABL": [
        "imatinib", "dasatinib", "nilotinib", "bosutinib", "ponatinib"
    ],
    "EML4-ALK": [
        "crizotinib", "alectinib", "ceritinib", "brigatinib", "lorlatinib"
    ]
}

# Cancer types that should be strictly excluded for specific searches
EXCLUDED_CANCER_TYPES = [
    # Digestive System
    "colorectal", "gastric", "esophageal", "pancreatic", "liver",
    "gallbladder", "cholangiocarcinoma", "bile duct",

    # Genitourinary System
    "prostate", "bladder", "kidney", "renal", "ovarian", "cervical",
    "endometrial", "uterine", "testicular", "penile",

    # Hematologic Malignancies
    "leukemia", "lymphoma", "myeloma", "hodgkin", "non-hodgkin",
    "acute myeloid leukemia", "chronic lymphocytic leukemia",

    # Other Solid Tumors
    "breast", "head and neck", "brain", "glioblastoma", "mesothelioma",
    "thyroid", "sarcoma", "melanoma", "neuroendocrine", "carcinoid",

    # Pediatric Cancers
    "neuroblastoma", "wilms tumor", "rhabdomyosarcoma", "ewing sarcoma"
]

# Pan-cancer trial keywords that indicate broad applicability
PAN_CANCER_KEYWORDS = [
    "solid tumor", "solid tumors", "advanced cancer", "metastatic cancer",
    "refractory cancer", "relapsed cancer", "any cancer type",
    "multiple cancer types", "pan-cancer", "tumor agnostic",
    "histology independent", "site agnostic", "basket trial",
    "umbrella trial", "precision medicine", "biomarker driven"
]

# Gene-focused trial keywords
GENE_FOCUSED_KEYWORDS = [
    "mutation", "positive", "amplification", "overexpression",
    "fusion", "rearrangement", "alteration", "variant",
    "biomarker", "targeted therapy", "precision oncology",
    "molecular profiling", "genetic testing", "companion diagnostic"
]

# Treatment stage mappings
TREATMENT_STAGE_SYNONYMS = {
    "first-line": [
        "first line", "1st line", "treatment-naive", "previously untreated",
        "initial treatment", "frontline", "naive", "treatment naive"
    ],

    "second-line": [
        "second line", "2nd line", "previously treated", "after progression",
        "post-progression", "relapsed", "recurrent"
    ],

    "third-line": [
        "third line", "3rd line", "heavily pretreated", "multiple prior",
        "salvage", "refractory", "treatment refractory"
    ]
}

# ECOG performance status descriptions
ECOG_DESCRIPTIONS = {
    "0": "fully active, able to carry on all pre-disease performance",
    "1": "restricted in physically strenuous activity but ambulatory",
    "2": "ambulatory and capable of all selfcare but unable to work",
    "3": "capable of only limited selfcare, confined to bed/chair >50% of time",
    "4": "completely disabled, cannot carry on any selfcare"
}


# Function to get all synonyms for a cancer type
def get_cancer_synonyms(cancer_type: str) -> list:
    """Get all synonyms for a given cancer type"""
    cancer_lower = cancer_type.lower()
    return CANCER_SYNONYMS.get(cancer_lower, [])


# Function to get all drugs for a gene mutation
def get_gene_drugs(gene: str) -> list:
    """Get all targeted drugs for a given gene mutation"""
    gene_upper = gene.upper()
    return GENE_DRUG_MAPPING.get(gene_upper, [])


# Function to check if a cancer type should be excluded
def is_excluded_cancer(cancer_type: str, user_cancers: list) -> bool:
    """Check if a cancer type should be excluded based on user's cancer types"""
    cancer_lower = cancer_type.lower()

    if cancer_lower in EXCLUDED_CANCER_TYPES:
        # Check if this excluded cancer matches any of user's cancers
        for user_cancer in user_cancers:
            user_cancer_lower = user_cancer.lower()
            if (cancer_lower in user_cancer_lower or
                    user_cancer_lower in cancer_lower or
                    any(synonym.lower() in user_cancer_lower
                        for synonym in get_cancer_synonyms(user_cancer))):
                return False  # Don't exclude if it matches user's cancer
        return True  # Exclude if no match with user's cancers

    return False


# Function to check if trial is pan-cancer
def is_pan_cancer_trial(title: str, inclusion: str) -> bool:
    """Check if a trial is pan-cancer based on keywords"""
    text = f"{title} {inclusion}".lower()
    return any(keyword in text for keyword in PAN_CANCER_KEYWORDS)


# Function to check if trial is gene-focused
def is_gene_focused_trial(title: str, inclusion: str, gene: str = None) -> bool:
    """Check if a trial is gene-focused"""
    text = f"{title} {inclusion}".lower()

    # General gene-focused keywords
    if any(keyword in text for keyword in GENE_FOCUSED_KEYWORDS):
        if gene:
            gene_lower = gene.lower()
            return gene_lower in text
        return True

    return False


