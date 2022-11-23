from app.services.job_record_functions.status import status
from app.services.job_record_functions.alembic_version import alembic_version

job_record_functions = {'alembic_version': alembic_version,
             'status': status,
             }