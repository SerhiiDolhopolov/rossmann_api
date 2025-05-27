from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import IPvAnyAddress, EmailStr

from app.redis import get_redis
from app.config import TAG_ADMIN


TAG_ADMIN_USERS_COUNT = "admin:users count 👥"

router_admin = APIRouter(prefix="/users_count", tags=[TAG_ADMIN, TAG_ADMIN_USERS_COUNT])
IP_COUNT_KEY = "ip_count"
EMAIL_COUNT_KEY = "email_count"


@router_admin.get(
    "/by_ip",
    summary="Return approximate quantity of users by IP.",
    response_model=int,
)
async def get_users_count_by_ip(redis=Depends(get_redis)):
    """Get the count of unique IP addresses."""
    count = redis.pfcount(IP_COUNT_KEY)
    return count


@router_admin.post(
    "/add_ip",
    summary="Add IP to count",
)
async def add_ip(
    ip: IPvAnyAddress = Body(example="192.168.123.130"),
    redis=Depends(get_redis),
):
    """Add an IP address to the HyperLogLog count."""
    try:
        redis.pfadd(IP_COUNT_KEY, str(ip))
        count = redis.pfcount(IP_COUNT_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding IP address: {str(e)}")
    return {
        "status": "success",
        "message": f"IP address {ip} added successfully",
        "count": count,
    }


@router_admin.delete(
    "/reset_ip",
    summary="Reset IP count",
)
async def reset_ip_count(redis=Depends(get_redis)):
    """Reset the HyperLogLog count."""
    try:
        redis.delete(IP_COUNT_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting IP count: {str(e)}")
    return {
        "status": "success",
        "message": "IP count reset successfully",
    }


@router_admin.get(
    "/by_email",
    summary="Return approximate quantity of users by email.",
    response_model=int,
)
async def get_users_count_by_email(redis=Depends(get_redis)):
    """Get the count of unique email addresses."""
    count = redis.pfcount(EMAIL_COUNT_KEY)
    return count


@router_admin.post(
    "/add_email",
    summary="Add email to count",
)
async def add_email(
    email: EmailStr = Body(example="example@example.com"),
    redis=Depends(get_redis),
):
    """Add an email address to the HyperLogLog count."""
    try:
        redis.pfadd(EMAIL_COUNT_KEY, str(email))
        count = redis.pfcount(EMAIL_COUNT_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding email address: {str(e)}")
    return {
        "status": "success",
        "message": f"Email address {email} added successfully",
        "count": count,
    }


@router_admin.delete(
    "/reset_email",
    summary="Reset email count",
)
async def reset_email_count(redis=Depends(get_redis)):
    """Reset the HyperLogLog email count."""
    try:
        redis.delete(EMAIL_COUNT_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting email count: {str(e)}")
    return {
        "status": "success",
        "message": "Email count reset successfully",
    }