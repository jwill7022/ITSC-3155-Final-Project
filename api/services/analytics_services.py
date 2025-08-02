import decimal

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from fastapi import HTTPException, status
from typing import List, Dict, Optional
from ..models.menu_items import MenuItem
from ..models.order_details import OrderDetail
from ..models.reviews import Reviews
from ..models.orders import Order

class AnalyticsService:

    @staticmethod
    def get_menu_item_performance(db: Session) -> List[Dict]:
        """
        Get performance analytics for menu items
        :param db:
        :return:
        """
        try:
            #Get order frequency and revenue per menu item
            performance_query = db.query(
                MenuItem.id,
                MenuItem.name,
                MenuItem.price,
                func.count(OrderDetail.id).label('order_count'),
                func.sum(OrderDetail.amount).label('total_quantity_sold'),
                (func.sum(OrderDetail.amount) * MenuItem.price).label('total_revenue'),
                func.avg(Reviews.rating).label('avg_rating'),
                func.count(Reviews.id).label('review_count')
            ).outerjoin(OrderDetail, MenuItem.id == OrderDetail.menu_item_id)\
            .outerjoin(Reviews, MenuItem.id == Reviews.menu_item_id)\
            .group_by(MenuItem.id, MenuItem.name, MenuItem.price)\
            .all()

            #Calculate popularity ranking
            results = []
            for item in performance_query:
                popularity_score = (item.order_count or 0) * decimal.Decimal(0.7) + (item.avg_rating or 0) * decimal.Decimal(0.3)

                results.append({
                    "menu_item_id": item.id,
                    "name": item.name,
                    "price": float(item.price),
                    "order_count": item.order_count or 0,
                    "total_quantity_sold": item.total_quantity_sold or 0,
                    "total_revenue": float(item.total_revenue or 0),
                    "average_rating": float(item.avg_rating) if item.avg_rating else None,
                    "review_count": item.review_count or 0,
                    "popularity_score": popularity_score,
                    "performance_status": AnalyticsService._get_performance_status(
                        item.order_count or 0,
                        item.avg_rating or 0
                    )
                })

            results.sort(key=lambda x: x['popularity_score'], reverse=True)

            return results

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Analytics query failed: {str(e)}"
            )

    @staticmethod
    def _get_performance_status(order_count: int, avg_rating: float) -> str:
        """Determine performance status based on metrics"""
        if order_count >= 50 and avg_rating > 4.0:
            return "excellent"
        elif order_count >= 20 and avg_rating > 3.5:
            return "good"
        elif order_count <5 or avg_rating < 2.5:
            return "poor"
        else:
            return "average"

    @staticmethod
    def get_review_insights(db: Session, menu_item_id: Optional[int] = None) -> Dict:
        """
        Get detailed review insights and identify problem areas
        :param db:
        :param menu_item_id:
        :return:
        """
        try:
            query = db.query(Reviews)
            if menu_item_id:
                query = query.filter(Reviews.menu_item_id == menu_item_id)

            reviews = query.all()

            if not reviews:
                return {
                    "total_reviews": 0,
                    "average_rating": 0,
                    "rating_distribution": {},
                    "recent_complaints": [],
                    "satisfaction_summary": "No reviews available"
                }

            #Calculate rating distribution
            rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            total_rating = 0
            complaint_keywords = ['bad', 'terrible', 'awful', 'disappointing', 'cold', 'slow', 'rude']
            complaints = []

            for review in reviews:
                rating_counts[review.rating] += 1
                total_rating += review.rating

                #Identify potential complaints (ratings 1-2 with text)
                if review.rating <= 2 and review.review_text:
                    text_lower = review.review_text.lower()
                    if any(keyword in text_lower for keyword in complaint_keywords):
                        complaints.append({
                            "customer_name": review.customer_name,
                            "rating": review.rating,
                            "review_text": review.review_text,
                            "created_at": review.created_at,
                            "menu_item_id": review.menu_item_id
                        })

            complaints.sort(key=lambda x: x['created_at'], reverse=True)

            avg_rating = total_rating / len(reviews)
            satisfaction_level = AnalyticsService._get_satisfaction_level(avg_rating, rating_counts)

            return {
                "total_reviews": len(reviews),
                "average_rating": round(avg_rating, 2),
                "rating_distribution": rating_counts,
                "recent_complaints": complaints[:10],  #Last 10 complaints only
                "satisfaction_summary": satisfaction_level,
                "recommendations": AnalyticsService._get_improvement_recommendations(
                    avg_rating, rating_counts, complaints
                )
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Review analysis failed: {str(e)}"
            )

    @staticmethod
    def _get_satisfaction_level(avg_rating: float, rating_counts: Dict) -> str:
        """Determine customer satisfaction level"""
        negative_reviews = rating_counts[1] + rating_counts[2]
        total_reviews = sum(rating_counts.values())
        negative_percentage = (negative_reviews / total_reviews) * 100 if total_reviews > 0 else 0

        if avg_rating >= 4.5 and negative_percentage < 10:
            return "Excellent - Customers are very satisfied"
        elif avg_rating >= 4.0 and negative_percentage < 20:
            return "Good - Most customers are satisfied"
        elif avg_rating >= 3.0:
            return "Average - Mixed customer feedback"
        else:
            return "Poor - Significant customer dissatisfaction"

    @staticmethod
    def _get_improvement_recommendations(avg_rating: float, rating_counts: Dict, complaints: List) -> List[str]:
        """Generate improvement recommendations based on data"""
        recommendations = []

        if avg_rating < 3.5:
            recommendations.append("Consider reviewing menu item quality and preparation")

        if rating_counts[1] + rating_counts[2] > rating_counts[4] + rating_counts[5]:
            recommendations.append("Focus on addressing negative feedback patterns")

        #Analyze complaint patterns
        complaint_text = ' '.join([c['review_text'].lower() for c in complaints if c['review_text']])

        if 'cold' in complaint_text or 'temperatuere' in complaint_text:
            recommendations.append("Review food temperature control and serving times")

        if 'slow' in complaint_text or 'wait' in complaint_text:
            recommendations.append("Improve order preparation and delivery times")

        if 'service' in complaint_text or 'staff' in complaint_text:
            recommendations.append("Provide additional customer service training")

        if not recommendations:
            recommendations.append("Continue monitoring customer feedback for improvement opportunities")

        return recommendations