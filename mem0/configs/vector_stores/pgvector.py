from typing import Optional

from pydantic import BaseModel, Field, model_validator

class PGVectorConfig(BaseModel):

    dbname: str = Field("postgres", description="Default name for the database")
    collection_name: str = Field("mem0", description="Default name for the collection")
    embedding_model_dims: Optional[int] = Field(1536, description="Dimensions of the embedding model")
    user: Optional[str] = Field(None, description="Database user")
    password: Optional[str] = Field(None, description="Database password")
    host: Optional[str] = Field("127.0.0.1", description="Database host. Default is localhost")
    port: Optional[int] = Field(5432, description="Database port. Default is 1536")

    @model_validator(mode="before")
    def check_user_and_password(cls, values):
        user, password = values.get("user"), values.get("password")
        if not user and not password:
            raise ValueError("Both 'user' and 'password' must be provided.")
        return values
    