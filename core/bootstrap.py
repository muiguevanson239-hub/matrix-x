from core.intelligent_db import IntelligentDB
from core.retrieval_engine import RetrievalEngine
from core.index_engine import IndexEngine
from core.api_gateway import APIGateway
from core.query_engine import QueryEngine
from core.tenant_db import TenantDB
from core.orchestrator import Orchestrator


class MatrixX:

    def __init__(self):

        # ---------------------------------
        # CORE DATABASE
        # ---------------------------------
        self.db = IntelligentDB()

        # ---------------------------------
        # RETRIEVAL LAYER
        # ---------------------------------
        self.retrieval = RetrievalEngine(self.db)

        # ---------------------------------
        # INDEX LAYER
        # ---------------------------------
        self.index = IndexEngine(self.db, self.retrieval)

        # build initial index
        self.index.build_index()

        # ---------------------------------
        # QUERY ENGINE
        # ---------------------------------
        self.query_engine = QueryEngine(
            self.db,
            self.index,
            self.retrieval
        )

        # ---------------------------------
        # TENANT SYSTEM
        # ---------------------------------
        self.tenants = TenantDB()

        # ---------------------------------
        # API GATEWAY
        # ---------------------------------
        self.gateway = APIGateway()

        # ---------------------------------
        # ORCHESTRATOR (CORE BRAIN)
        # ---------------------------------
        self.orchestrator = Orchestrator(
            self.gateway,
            self.tenants,
            self.query_engine
        )

    # ---------------------------------
    # SINGLE ENTRY POINT
    # ---------------------------------
    def handle(self, api_key, tenant_id, query):

        return self.orchestrator.handle(
            api_key,
            tenant_id,
            query
        )