import json

from fastapi import APIRouter, HTTPException
from fastapi import Depends, Query
from pydantic import EmailStr
from rossmann_users_db_models import User

from app.redis import get_redis
from app.users_db import get_db
from app.schemas import UserSchema, UserAddSchema, UserPatchSchema


TAG_USERS = 'users 👤'

router = APIRouter(prefix='/users', tags=[TAG_USERS])


@router.get('/', response_model=list[UserSchema])
def get_users(skip: int = Query(0, ge=0),
              limit: int = Query(100, gt=0, le=100),
              db=Depends(get_db)):
    users = db.query(User) \
              .offset(skip) \
              .limit(limit) \
              .all()
    return users

@router.get('/{user_id:int}', response_model=UserSchema)
def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(User) \
             .filter(User.user_id == user_id) \
             .first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post('/', response_model=UserSchema)
def add_user(user: UserAddSchema, db=Depends(get_db)):
    user = User(**user.model_dump())
    if db.query(User) \
         .filter(User.email == user.email) \
         .first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch('/{user_id:int}', response_model=UserSchema)
def update_user(user_id: int, user: UserPatchSchema, db=Depends(get_db)):
    existing_user = db.query(User) \
                      .filter(User.user_id == user_id) \
                      .first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(existing_user, key, value)
    
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.get('/authorize/{user_email}')
def authorize_user(user_email: EmailStr, 
                   password: str, 
                   db=Depends(get_db)):
    user = db.query(User) \
             .filter(User.email == user_email) \
             .first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {'success': 'ok', 'user': user}


def get_shopping_cart_key(user_id: int) -> str:
    return f"shopping_cart:{user_id}"

@router.get('/{user_id:int}/shopping_cart', summary='Return dict of shopping card. {product_id: count}', response_model=dict)
def get_shopping_cart(user_id: int, redis=Depends(get_redis)):
    shopping_cart = redis.get(get_shopping_cart_key(user_id))
    if not shopping_cart:
        return {}
    return json.loads(shopping_cart)

@router.patch('/{user_id:int}/shopping_cart', 
              summary='Update a product in the user\'s shopping cart. If quantity=0, remove the product. Update cart lifetime to 24 hours.', 
              response_model=dict)
def update_shopping_cart(user_id: int, product_id: int, quantity: int, redis=Depends(get_redis)):
    shopping_cart_key = get_shopping_cart_key(user_id)
    shopping_cart = redis.get(shopping_cart_key)
    if not shopping_cart:
        shopping_cart = {}
    else:
        shopping_cart = json.loads(shopping_cart)
    
    shopping_cart[str(product_id)] = quantity
    if quantity == 0:
        del shopping_cart[str(product_id)]
    
    redis.set(shopping_cart_key, json.dumps(shopping_cart), ex=24 * 60 * 60)
    return {'success': 'ok', 'shopping_cart': shopping_cart}

