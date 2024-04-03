from fastapi import HTTPException, status

exception_auth = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

exception_user_not_found = HTTPException(status_code=404, detail="User not found")

exception_unique_field = HTTPException(
    status_code=400, detail="Unique field already exists."
)