
from docassemble.webapp.db_object import init_sqlalchemy
# db is a SQLAlchemy Engine
from sqlalchemy.sql import text
from typing import List, Tuple, Dict, Optional
from docassemble.base.util import user_has_privilege
import re


db = init_sqlalchemy()

__all__ = [
    "legalserver_get_sessions",
]


def legalserver_get_sessions(
    user_id: Optional[int] = None,
    filename: Optional[str] = None,
    filter_step1: bool = True,
    metadata_key_name: str = "metadata",
) -> List[Tuple]:
    """
    Return a list of the most recent 500 sessions, optionally tied to a specific user ID.

    Each session is a tuple with named columns:
    filename,
    user_id,
    modtime,
    key
    """
    get_sessions_query = text(
        """
SELECT 
    userdict.filename as filename,
    num_keys,
    userdictkeys.user_id as user_id,
    mostrecent.modtime as modtime,  -- This retrieves the most recent modification time for each key
    userdict.key as key,
    jsonstorage.data->>'auto_title' as auto_title,
    jsonstorage.data->>'title' as title,
    jsonstorage.data->>'description' as description,
    jsonstorage.data->>'steps' as steps,
    jsonstorage.data->>'progress' as progress
FROM 
    userdict 
NATURAL JOIN 
    (
        SELECT 
            key,
            MAX(modtime) AS modtime,  -- Calculate the most recent modification time for each key
            COUNT(key) AS num_keys
        FROM 
            userdict
        GROUP BY 
            key
        HAVING 
            COUNT(key) > 1 OR :filter_step1 = False
    ) mostrecent
LEFT JOIN 
    userdictkeys ON userdictkeys.key = userdict.key
LEFT JOIN 
    jsonstorage ON jsonstorage.key = userdict.key AND jsonstorage.tags = :metadata
WHERE 
    (userdict.user_id = :user_id OR :user_id is null)
    AND (userdict.filename = :filename OR :filename is null)
ORDER BY 
    modtime DESC 
LIMIT 500;
        """
    )
    if not filename:
        if not user_has_privilege(["admin", "developer"]):
            raise Exception(
                "You must provide a filename to filter sessions unless you are a developer or administrator."
            )
        filename = None  # Explicitly treat empty string as equivalent to None
    if not user_id:
        user_id = None

    # Ensure filter_step1 is a boolean
    filter_step1 = bool(filter_step1)

    with db.connect() as con:
        rs = con.execute(
            get_sessions_query,
            {
                "user_id": user_id,
                "filename": filename,
                "filter_step1": filter_step1,
                "metadata": metadata_key_name,
            },
        )
    sessions = [session for session in rs]

    return sessions

