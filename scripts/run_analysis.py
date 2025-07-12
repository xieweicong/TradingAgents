#!/usr/bin/env python3
"""
Enhanced Trading Agents - 主分析脚本

使用示例:
    python scripts/run_analysis.py --stocks AAPL,NVDA --date 2025-07-12
    python scripts/run_analysis.py --stock-list test_stocks
"""

import sys
import os
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from extensions.multi_stock.analyzer import MultiStockAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Enhanced Trading Agents Analysis")
    parser.add_argument("--stocks", help="Comma-separated list of stock symbols")
    parser.add_argument("--stock-list", help="Predefined stock list name") 
    parser.add_argument("--date", help="Analysis date (YYYY-MM-DD)")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker threads")
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = MultiStockAnalyzer(max_workers=args.workers)
    
    # 确定股票列表
    if args.stocks:
        stock_list = args.stocks.split(",")
        results = analyzer.analyze_stocks(
            stock_list=stock_list,
            analysis_date=args.date,
            save_results=True
        )
    elif args.stock_list:
        results = analyzer.analyze_stocks(
            stock_list_name=args.stock_list,
            analysis_date=args.date,
            save_results=True
        )
    else:
        # 交互模式
        print("进入交互模式...")
        # 实现交互逻辑

if __name__ == "__main__":
    main()
