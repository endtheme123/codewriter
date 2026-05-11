from config import settings

from packages.ai.claude import ClaudeProvider
from packages.ai.vllm import VLLMProvider
from packages.ai.dummy import MockProvider
from packages.ai.litellm import LiteLLMProvider

from knowledge_base.embedding.st_embed import SentenceTransformerEmbedder
from knowledge_base.vector_db.faiss import FaissVectorStore
from knowledge_base.main import KnowledgeBase
from knowledge_base.ingest import KnowledgeIngestor

from database.excel import ExcelRiskRepository

from packages.service.chat_service import ChatService


def create_provider():
    if settings.LLM_PROVIDER == "claude":
        return ClaudeProvider()

    elif settings.LLM_PROVIDER == "vllm":
        return VLLMProvider()

    elif settings.LLM_PROVIDER == "litellm":
        return LiteLLMProvider()

    elif settings.LLM_PROVIDER == "mock":
        return MockProvider()

    raise ValueError("Unsupported provider")



# -------------------------
# SINGLETONS
# -------------------------


db = ExcelRiskRepository(file_path="/home/nguyen.ha.huy.hoang/git/excel_repo/test_data.xlsx")

provider = create_provider()

embedder = SentenceTransformerEmbedder()

sample = embedder.embed("hello")
dimension = len(sample)
print(f"Embedding dimension: {dimension}")

vector_store = FaissVectorStore(
    dimension=dimension
)

knowledge_base = KnowledgeBase(
    embedder=embedder,
    vector_store=vector_store
)

chat_service = ChatService(
    provider=provider,
    knowledge_base=knowledge_base
)


# -------------------------
# INGEST DOCUMENTS
# -------------------------

ingestor = KnowledgeIngestor(
    knowledge_base=knowledge_base
)

ingestor.ingest_directory("./knowledge_base/knowledge_storage")