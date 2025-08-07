from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from typing import List, Optional, Dict
from ..models.menu_items import MenuItem, FoodCategory
from ..models.reviews import Reviews
from sqlalchemy import func


class MenuService:

    @staticmethod
    def search_menu_items(
            db: Session,
            search_term: Optional[str] = None,
            category: Optional[FoodCategory] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            max_calories: Optional[int] = None,
            sort_by: str = "name",
            available_only: bool = True
    ) -> List[Dict]:
        """
        Search and filter menu items.
        :param db:
        :param search_term:
        :param category:
        :param min_price:
        :param max_price:
        :param max_calories:
        :param sort_by:
        :param available_only:
        :return:
        """
        try:
            query = db.query(MenuItem)

            # Filter by availability
            if available_only:
                query = query.filter(MenuItem.is_available == True)

            # Apply filters
            if search_term:
                query = query.filter(
                    or_(
                        MenuItem.name.ilike(f"%{search_term}%"),
                        MenuItem.description.ilike(f"%{search_term}%")
                    )
                )

            if category:
                query = query.filter(MenuItem.food_category == category)

            if min_price is not None:
                query = query.filter(MenuItem.price >= min_price)

            if max_price is not None:
                query = query.filter(MenuItem.price <= max_price)

            if max_calories is not None:
                query = query.filter(MenuItem.calories <= max_calories)

            # Apply sorting
            if sort_by == "price_asc":
                query = query.order_by(MenuItem.price.asc())
            elif sort_by == "price_desc":
                query = query.order_by(MenuItem.price.desc())
            elif sort_by == "calories":
                query = query.order_by(MenuItem.calories.asc())
            elif sort_by == "rating":
                #Subquery for rating sort
                avg_rating_subquery = db.query(
                    Reviews.menu_item_id,
                    func.avg(Reviews.rating).label('avg_rating')
                ).group_by(Reviews.menu_item_id).subquery()

                query = query.outerjoin(
                    avg_rating_subquery,
                    MenuItem.id == avg_rating_subquery.c.menu_item_id
                ).order_by(avg_rating_subquery.c.avg_rating.desc().nullslast())
            else:  # default to name
                query = query.order_by(MenuItem.name.asc())

            items = query.all()

            # Add review stats
            result = []
            for item in items:
                avg_rating = db.query(func.avg(Reviews.rating)).filter(
                    Reviews.menu_item_id == item.id
                ).scalar()

                review_count = db.query(func.count(Reviews.id)).filter(
                    Reviews.menu_item_id == item.id
                ).scalar()

                result.append({
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "price": float(item.price),
                    "calories": item.calories,
                    "food_category": item.food_category.value,
                    "is_available": item.is_available,
                    "average_rating": float(avg_rating) if avg_rating else None,
                    "review_count": review_count or 0
                })

            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Search failed: {str(e)}"
            )