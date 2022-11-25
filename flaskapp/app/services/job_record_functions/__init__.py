from app.services.job_record_functions.status import status
from app.services.job_record_functions.alembic_version import alembic_version
from app.services.job_record_functions.database_connection import database_connection

job_record_functions = {
        'alembic_version': alembic_version,
        'status': status,
        'database_connection':database_connection
             }