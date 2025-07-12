#!/usr/bin/env python3
"""
Multi-Stock Analyzer Usage Examples

This file demonstrates different ways to use the multi-stock analyzer.
"""

from extensions.multi_stock.analyzer import MultiStockAnalyzer, StockListManager
from datetime import datetime, timedelta

def example_basic_usage():
    """Basic usage example - analyze default test stocks"""
    print("=== 基础使用示例 ===")
    
    # Initialize analyzer with default settings (using 1 worker to avoid memory conflicts)
    analyzer = MultiStockAnalyzer(max_workers=1)
    
    # Analyze test stocks (default configuration)
    results = analyzer.analyze_stocks(
        stock_list_name="test_stocks",  # Uses predefined test list
        analysis_date="2025-07-12",
        save_results=True
    )
    
    print(f"分析完成，共分析了 {len(results)} 只股票")
    return results

def example_custom_stock_list():
    """Example with custom stock list"""
    print("\n=== 自定义股票列表示例 ===")
    
    analyzer = MultiStockAnalyzer(max_workers=3)
    
    # Create custom stock list
    custom_stocks = ['AAPL', 'MSFT', 'GOOGL']
    
    results = analyzer.analyze_stocks(
        stock_list=custom_stocks,
        analysis_date="2025-07-12", 
        save_results=True
    )
    
    print(f"自定义列表分析完成，共分析了 {len(results)} 只股票")
    return results

def example_manage_stock_lists():
    """Example of managing stock lists"""
    print("\n=== 股票列表管理示例 ===")
    
    analyzer = MultiStockAnalyzer()
    
    # Add a new stock list
    tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA']
    analyzer.add_stock_list("tech_giants", tech_stocks)
    
    # Show all available lists
    available_lists = analyzer.get_available_stock_lists()
    print("可用的股票列表:")
    for list_name, stocks in available_lists.items():
        print(f"  {list_name}: {stocks}")
    
    # Use the new list
    results = analyzer.analyze_stocks(
        stock_list_name="tech_giants",
        save_results=True
    )
    
    return results

def example_custom_config():
    """Example with custom configuration"""
    print("\n=== 自定义配置示例 ===")
    
    # Create custom configuration
    custom_config = {
        "llm_provider": "deepseek",
        "backend_url": "https://api.deepseek.com/v1",
        "deep_think_llm": "deepseek-reasoner",
        "quick_think_llm": "deepseek-chat",
        "max_debate_rounds": 2,  # More thorough analysis
        "online_tools": True
    }
    
    analyzer = MultiStockAnalyzer(config=custom_config, max_workers=2)
    
    results = analyzer.analyze_stocks(
        stock_list=['NVDA', 'AMD'],
        analysis_date="2025-07-12",
        save_results=True
    )
    
    print(f"自定义配置分析完成")
    return results

def example_batch_historical_analysis():
    """Example of analyzing multiple dates"""
    print("\n=== 批量历史分析示例 ===")
    
    analyzer = MultiStockAnalyzer(max_workers=3)
    
    # Analyze same stocks for multiple dates
    stocks = ['AAPL', 'NVDA']
    dates = [
        "2025-07-10",
        "2025-07-11", 
        "2025-07-12"
    ]
    
    all_results = {}
    
    for date in dates:
        print(f"\n分析日期: {date}")
        results = analyzer.analyze_stocks(
            stock_list=stocks,
            analysis_date=date,
            save_results=True
        )
        all_results[date] = results
    
    print(f"\n批量分析完成，共分析了 {len(dates)} 个日期")
    return all_results

def example_result_analysis():
    """Example of analyzing results after completion"""
    print("\n=== 结果分析示例 ===")
    
    analyzer = MultiStockAnalyzer(max_workers=2)
    
    results = analyzer.analyze_stocks(
        stock_list=['AAPL', 'NVDA'],
        save_results=True
    )
    
    # Analyze results
    print("\n详细结果分析:")
    for ticker, result in results.items():
        print(f"\n--- {ticker} ---")
        print(f"状态: {result.status}")
        print(f"处理时间: {result.total_processing_time:.2f}秒")
        
        if result.status == "completed":
            print(f"分析师报告数量: {len(result.analyst_outputs)}")
            print(f"研究团队报告数量: {len(result.research_outputs)}")
            print(f"有交易员报告: {'是' if result.trader_output else '否'}")
            print(f"风险管理报告数量: {len(result.risk_outputs)}")
            print(f"有投资组合决策: {'是' if result.portfolio_output else '否'}")
            
            if result.final_decision:
                print(f"最终决策摘要: {result.final_decision[:200]}...")
        else:
            print(f"错误信息: {result.error_message}")
    
    return results

def example_jp_stocks():
    """Example of analyzing Japanese stocks"""
    print("\n=== 日本股票分析示例 ===")
    
    analyzer = MultiStockAnalyzer(max_workers=2)
    
    # Add Japanese stocks list if not exists
    jp_stocks = ['7203.T', '6758.T', '9984.T']  # Toyota, Sony, SoftBank
    analyzer.add_stock_list("jp_test", jp_stocks)
    
    results = analyzer.analyze_stocks(
        stock_list_name="jp_test",
        analysis_date="2025-07-12",
        save_results=True
    )
    
    print(f"日本股票分析完成")
    return results

def main():
    """Run all examples"""
    print("Multi-Stock Analyzer 使用示例")
    print("=" * 50)
    
    try:
        # Run basic example
        example_basic_usage()
        
        # Run other examples (comment out if you want to run only one)
        # example_custom_stock_list()
        # example_manage_stock_lists()
        # example_custom_config()
        # example_result_analysis()
        # example_jp_stocks()
        
        # Uncomment for batch analysis (takes longer)
        # example_batch_historical_analysis()
        
        print("\n" + "=" * 50)
        print("所有示例完成！")
        print("检查 multi_analysis_results/ 和 multi_analysis_logs/ 目录查看结果")
        
    except Exception as e:
        print(f"示例运行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()