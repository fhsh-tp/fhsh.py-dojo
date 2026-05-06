"""Configuration for lit-fetcher."""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent
_output_env = os.getenv("OUTPUT_DIR", "")
OUTPUT_DIR = Path(_output_env).resolve() if _output_env else (PROJECT_ROOT / ".." / ".." / "refs").resolve()

FJU_PROXY_USER = os.getenv("FJU_PROXY_USER", "")
FJU_PROXY_PASS = os.getenv("FJU_PROXY_PASS", "")
FJU_PROXY_HOST = os.getenv("FJU_PROXY_HOST", "authproxy.fju.edu.tw")
FJU_PROXY_PORT = int(os.getenv("FJU_PROXY_PORT", "3128"))

SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
SEARCH_YEAR_MIN = int(os.getenv("SEARCH_YEAR_MIN", "2024"))
SEARCH_YEAR_MAX = int(os.getenv("SEARCH_YEAR_MAX", "2026"))

APPROVED_CONFERENCES = [
    "ICML", "NeurIPS", "IJCNN", "AAAI", "IJCAI", "ICLR", "CVPR", "ICCV",
    "International Conference on Machine Learning",
    "Neural Information Processing Systems",
    "International Joint Conference on Neural Networks",
    "Association for the Advancement of Artificial Intelligence",
    "International Joint Conference on Artificial Intelligence",
    "International Conference on Learning Representations",
    "Computer Vision and Pattern Recognition",
    "International Conference on Computer Vision",
]

APPROVED_Q1_JOURNALS = [
    "Nature Machine Intelligence",
    "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "Information Fusion",
    "Artificial Intelligence Review",
    "IEEE Transactions on Image Processing",
    "IEEE Transactions on Evolutionary Computation",
    "IEEE Transactions on Fuzzy Systems",
    "Medical Image Analysis",
    "IEEE Transactions on Cybernetics",
    "IEEE Transactions on Knowledge and Data Engineering",
    "International Journal of Computer Vision",
    "IEEE Transactions on Neural Networks and Learning Systems",
    "Neural Networks",
    "Neurocomputing",
    "Pattern Recognition",
    "Knowledge-Based Systems",
    "Expert Systems with Applications",
    "Applied Soft Computing",
    "ACM Transactions on Intelligent Systems and Technology",
    "Transactions of the Association for Computational Linguistics",
    "Journal of Machine Learning Research",
    "Engineering Applications of Artificial Intelligence",
    "Advanced Engineering Informatics",
    "Swarm and Evolutionary Computation",
    "IEEE Intelligent Systems",
    "Computational Linguistics",
    "Integrated Computer-Aided Engineering",
    "Foundations and Trends in Machine Learning",
    "AI Open",
    "CAAI Transactions on Intelligence Technology",
    "Machine Intelligence Research",
    "Big Data Mining and Analytics",
    "Artificial Intelligence in Medicine",
    "Advanced Intelligent Systems",
    "Robotics and Autonomous Systems",
]
