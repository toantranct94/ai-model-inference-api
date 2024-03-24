import re
from typing import List

from fastapi import HTTPException, UploadFile

from app.cores import strings


class UploadImageValidator:
    """Validate the file to be uploaded.

    Raises:
        HTTPException: If the file is not in allowed types
            or exceeds the maximum size.
    """

    MEDIA_ALLOWED_TYPES = ['image']
    MAX_SIZE = 100 * 1024 * 1024  # 100mb

    def __init__(
        self,
        media_allowed_types: List[str] = MEDIA_ALLOWED_TYPES,
        max_size: int = MAX_SIZE
    ):
        self.media_allowed_types = media_allowed_types
        self.max_size = max_size

    def __call__(self, image: UploadFile):

        content_type = re.search(r'^([\w]+)/', image.content_type).group(1)
        if content_type not in self.media_allowed_types:
            raise HTTPException(400, strings.INVALID_CONTENT_TYPE)

        if image.size > self.max_size:
            raise HTTPException(400, strings.EXCEED_MAX_SIZE)
