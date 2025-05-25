from typing import Dict, Any, List, Optional
import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def sanitize_string(text: str) -> str:
    if not text:
        return ""
    return text.strip()


def paginate_query(query, page: int = 1, per_page: int = 10):
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page)


def create_response(
    success: bool = True,
    message: str = "",
    data: Any = None,
    errors: Optional[Dict] = None,
) -> Dict[str, Any]:
    response = {
        "success": success,
        "message": message,
        "data": data,
    }

    if errors:
        response["errors"] = errors

    return response
