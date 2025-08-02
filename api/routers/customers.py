from fastapi import APIRouter, Depends, status, Response, Query, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..schemas.common import PaginationParams, PaginatedResponse
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Customers'],
    prefix="/customers",
    responses={
        404: {"description": "Customer not found"},
        400: {"description": "Invalid input data"},
        409: {"description": "Customer already exists"}
    }
)

@router.post(
    "/",
    response_model=schema.Customer,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer",
    description="Register a new customer with validated contact information",
    responses={
        201: {"description": "Customer created successfully"},
        409: {"description": "Customer with this email or phone already exists"}
    }
)
def create_customer(
        request: schema.CustomerCreate,
        db: Session = Depends(get_db)
) -> schema.Customer:
    """
    Create a new customer with the following information:

    - **customer_name**: Full name (2-100 characters)
    - **customer_email**: Valid email address (optional)
    - **customer_phone**: 10-digit US phone number
    - **customer_address**: Full address (optional, max 200 characters)
    :param request:
    :param db:
    :return:
    """
    return controller.create(db=db, request=request)

@router.get(
    "/",
    response_model=list[schema.Customer],
    summary="Get all customers",
    description="Retrieve a paginated list of all customers"
)
def get_customers(
        skip: int = Query(0, ge=0, description="Number of customers to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of customers to return"),
        search: Optional[str] = Query(None, description="Search customers by name or email"),
        db: Session = Depends(get_db)
) -> List[schema.Customer]:
    """
    Get all customers with optional search and pagination:

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **search**: Search term for name or email filtering
    :param skip:
    :param limit:
    :param search:
    :param db:
    :return:
    """
    if search:
        return controller.search_customers(db, search, skip, limit)
    return controller.read_all(db, skip, limit)


@router.get(
    "/{customer_id}",
    response_model=schema.Customer,
    description="Retrieve a specific customer by their ID"
)
def get_customer(
        customer_id: int = Path(..., gt=0, description="Customer ID"),
        db: Session = Depends(get_db)
) -> schema.Customer:
    return controller.read_one(db, item_id=customer_id)


@router.put(
    "/{customer_id}",
    response_model=schema.Customer,
    summary="Update customer",
    description="Update customer information")
def update_customer(
        customer_id: int = Path(..., gt=0, description="Customer ID"),
        request: schema.CustomerUpdate = ...,
        db: Session = Depends(get_db)
) -> schema.Customer:
    """
    Update customer information:

    - All fields are optional
    - Only provided fields will be updated
    - Phone number must be valid US format if provided
    :param customer_id:
    :param request:
    :param db:
    :return:
    """
    return controller.update(db=db, request=request, item_id=customer_id)


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete customer",
    description="Delete a customer (only if no active orders)"
)
def delete_customer(
        customer_id: int = Path(..., gt=0, description="Customer ID"),
        db: Session = Depends(get_db)
):
    return controller.delete(db=db, item_id=customer_id)