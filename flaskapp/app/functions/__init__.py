from app.functions.backend.status import status
from app.functions.database.alembic_version import alembic_version

functions = {'alembic_version': alembic_version,
             'status': status,
             }