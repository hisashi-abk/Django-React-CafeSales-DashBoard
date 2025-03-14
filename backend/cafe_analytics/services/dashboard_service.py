from typing import Dict, List, Optional, Any, Union
from datetime import date, datetime, timedelta

from cafe_analytics.models import Order
from . import BaseService
from .sales_service import SalesService
from .order_service import OrderService
from .product_service import ProductService

class DashboardService(BaseService):
    """ダッシュボード表示に必要なデータを提供するサービス"""

    @classmethod
    def get_daily_dashboard(cls, target_date: Union[str, date]) -> Dict[str, Any]:
        """デイリーダッシュボード用のデータを取得"""
        target_date_obj = cls.parse_date_param(target_date) if not isinstance(target_date, date) else target_date
        if not target_date_obj:
            raise ValueError("Invalid date format")

        orders = OrderService.get_orders_in_period(target_date_obj, target_date_obj)
        sales_summary = SalesService.get_sales_summary(target_date_obj, target_date_obj)

        return {
            'date': target_date_obj,
            'sales_summary': sales_summary,
            'orders': OrderService.get_orders_summary(orders),
            'takeout_rate': SalesService.calculate_takeout_rate(orders),
            'popular_items': SalesService.get_top_categories(limit=5, start_date=target_date_obj, end_date=target_date_obj),
            'customer_count': sales_summary['total_orders'],
            'avg_order_value': sales_summary['avg_order_value'],
            'total_discount': sales_summary['total_discount'],
            'hourly_sales': SalesService.get_hourly_sales(orders),
            'customer_demographics': OrderService.get_customer_demographics(orders)
        }

    @classmethod
    def get_weekly_dashboard(cls, target_date: Union[str, date]) -> Dict[str, Any]:
        """ウィークリーダッシュボード用のデータを取得"""
        target_date_obj = cls.parse_date_param(target_date) if not isinstance(target_date, date) else target_date
        if not target_date_obj:
            raise ValueError("Invalid date format")

        start_date, end_date = OrderService.get_date_range(target_date_obj, 'week')
        orders = OrderService.get_orders_in_period(start_date, end_date)
        sales_summary = SalesService.get_sales_summary(start_date, end_date)

        return {
            'week_start': start_date,
            'week_end': end_date,
            'sales_summary': sales_summary,
            'weather_distribution': OrderService.get_weather_distribution(orders),
            'orders': OrderService.get_orders_summary(orders),
            'takeout_rate': SalesService.calculate_takeout_rate(orders),
            'popular_items': SalesService.get_top_categories(limit=5, start_date=start_date, end_date=end_date),
            'customer_count': sales_summary['total_orders'],
            'avg_order_value': sales_summary['avg_order_value'],
            'total_discount': sales_summary['total_discount'],
            'daily_sales_breakdown': SalesService.get_period_sales('daily', start_date, end_date),
            'customer_demographics': OrderService.get_customer_demographics(orders)
        }

    @classmethod
    def get_monthly_dashboard(cls, target_date: Union[str, date]) -> Dict[str, Any]:
        """マンスリーダッシュボード用のデータを取得"""
        target_date_obj = cls.parse_date_param(target_date) if not isinstance(target_date, date) else target_date
        if not target_date_obj:
            raise ValueError("Invalid date format")

        start_date, end_date = OrderService.get_date_range(target_date_obj, 'month')
        orders = OrderService.get_orders_in_period(start_date, end_date)
        sales_summary = SalesService.get_sales_summary(start_date, end_date)

        return {
            'month_start': start_date,
            'month_end': end_date,
            'sales_summary': sales_summary,
            'weather_distribution': OrderService.get_weather_distribution(orders),
            'orders': OrderService.get_orders_summary(orders),
            'takeout_rate': SalesService.calculate_takeout_rate(orders),
            'popular_items': SalesService.get_top_categories(limit=5, start_date=start_date, end_date=end_date),
            'customer_count': sales_summary['total_orders'],
            'avg_order_value': sales_summary['avg_order_value'],
            'total_discount': sales_summary['total_discount'],
            'weekly_sales_breakdown': SalesService.get_period_sales('weekly', start_date, end_date),
            'customer_demographics': OrderService.get_customer_demographics(orders)
        }
