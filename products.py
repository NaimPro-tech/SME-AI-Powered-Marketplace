from fastapi import APIRouter, Depends, HTTPException, status
from database import database
from schemas import ProductCreate, ProductResponse
from security import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

#endpoint of new product(Only for sellers)
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, current_user: dict = Depends(get_current_user)):
    # if current user is seller 
    if current_user.get("role") != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add products."
        )
        
    query = """INSERT INTO products (title, description, base_price, discount_price, is_offer_active, seller_id, category)
               VALUES(:title, :description, :base_price, :discount_price, :is_offer_active, :seller_id, :category)
               RETURNING product_id, title, description, base_price, discount_price, is_offer_active, seller_id, category, view_count, sales_count, created_at"""
               
    values = {
        "title": product.title,
        "description": product.description,
        "base_price": product.base_price,
        "discount_price": product.discount_price,
        "is_offer_active": product.is_offer_active,
        "seller_id": current_user.get("user_id"), # get user id from payload(token)
        "category": product.category
    }

    # insert product into database
    new_product = await database.fetch_one(query=query, values=values)
    
    # fetch name and info of seller
    user_query = "SELECT name, email FROM users WHERE user_id = :user_id"
    seller_info = await database.fetch_one(query=user_query, values={"user_id": current_user.get("user_id")})
    
    
    response_data = dict(new_product)
    response_data["seller"] = {
        "user_id":current_user.get("user_id"),
        "name": seller_info["name"],
        "email": seller_info["email"]
    }
    
    return response_data

@router.get("/", response_model=list[ProductResponse])
async def get_all_products():
    query = """SELECT p.*, u.user_id, u.name, u.email
                FROM products p
                JOIN users u ON p.seller_id = u.user_id"""
    rows =  await database.fetch_all(query=query)
    formatted_products = []
    for row in rows:
        product_dict = dict(row)
        product_dict["seller"] = {
            "user_id":row["user_id"],
            "name":row["name"],
            "email":row["email"]
        }
        formatted_products.append(product_dict)

    return formatted_products

#search by product id endpoint
@router.get("/{product_id}", response_model=ProductResponse)
async def get_single_product(product_id: int):
    #check the product is in database and sql join to get info of user also
    query = """SELECT p.*, u.user_id, u.name, u.email
                FROM products p
                JOIN users u ON p.seller_id = u.user_id
                WHERE  p.product_id = :product_id"""
    row = await database.fetch_one(query=query, values={"product_id": product_id})


    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Prouct not found"
        )
    #we can update our view count by time of views(future ml models feature -product insights)
    update_view_query = "UPDATE products SET view_count = view_count+1 WHERE product_id = :product_id"
    await database.execute(query=update_view_query, values={"product_id": product_id})

    #to match the data with pydantic format
    product = dict(row)
    product["seller"] = {
        "user_id":row["user_id"],
        "name":row["name"],
        "email":row["email"]
    }
    return product

#product update endpoint
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, current_user: dict = Depends(get_current_user)):

    #check if the product in database
    find_query = "SELECT * FROM products WHERE product_id = :product_id"
    existing_product = await database.fetch_one(query=find_query, values={"product_id": product_id})
    if existing_product["seller_id"] != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_query = """
            UPDATE products 
            SET title = :title, description = :description, base_price = :base_price, 
                discount_price = :discount_price, is_offer_active = :is_offer_active, category = :category
            WHERE product_id = :product_id
            RETURNING product_id, title, description, base_price, discount_price, is_offer_active, seller_id, category, view_count, sales_count, created_at
        """
    
    values = {
        "product_id": product_id,
        "title": product.title,
        "description": product.description,
        "base_price": product.base_price,
        "discount_price": product.discount_price,
        "is_offer_active": product.is_offer_active,
        "category": product.category
    }


    updated_product = await database.fetch_one(query=update_query, values=values)

    user_query = "SELECT name, email FROM users WHERE user_id = :user_id"
    user_data = await database.fetch_one(query=user_query, values={"user_id": current_user.get("user_id")})

    updated_product_list = dict(updated_product)
    updated_product_list['seller'] = {
        "user_id":current_user.get("user_id"),
        "name":user_data["name"],
        "email":user_data["email"]
    }
    return updated_product_list

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, current_user: dict = Depends(get_current_user)):

    #check if product
    find_query = "SELECT * FROM products WHERE product_id = :product_id"
    existing_product = await database.fetch_one(query=find_query, values={"product_id": product_id})

    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if existing_product["seller_id"] != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this product to delete it."
        )
    
    delete_query = "DELETE FROM products WHERE product_id = :product_id"
    await database.execute(query=delete_query, values={"product_id": product_id})

    return {"message": 'Product deleted successfully.'}
