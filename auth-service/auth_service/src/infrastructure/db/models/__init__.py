# __all__ = ("role_table", "user_table", "client_table", "strategy_table")
__all__ = ("role_table", "user_table", "client_table", "rs_table")

from infrastructure.db.models.client_models import client_table
from infrastructure.db.models.role_models import role_table

# from infrastructure.db.models.strategy_models import strategy_table
from infrastructure.db.models.user_models import user_table
from infrastructure.db.models.rs_models import rs_table
