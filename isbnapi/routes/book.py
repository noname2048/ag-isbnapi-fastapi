from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="book", tags=["book"])
