from pydantic import BaseModel, Field


class Token(BaseModel):
    """Response Token."""

    access_token: str = Field(description="JWT token.")
    token_type: str = Field(default="bearer", description="Token type.", pattern="bearer")
