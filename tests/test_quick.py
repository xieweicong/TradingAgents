#!/usr/bin/env python3
"""
Quick test of the multi-stock analyzer with memory fixes
"""

from multi_stock_analyzer import MultiStockAnalyzer

def test_basic():
    """Basic test with minimal configuration"""
    print("开始快速测试...")
    
    # Create custom configuration for testing
    import os
    test_config = {
        "llm_provider": "deepseek",
        "backend_url": "https://api.deepseek.com/v1", 
        "deep_think_llm": "deepseek-chat",  # Use faster model
        "quick_think_llm": "deepseek-chat",
        "max_debate_rounds": 1,
        "online_tools": True,
        "disable_memory": True,  # Disable memory to avoid conflicts
        "project_dir": os.getcwd()  # Add required project_dir
    }
    
    # Initialize analyzer with test config
    analyzer = MultiStockAnalyzer(config=test_config, max_workers=1)
    
    # Test with single stock
    results = analyzer.analyze_stocks(
        stock_list=['AAPL'],  # Just one stock for quick test
        analysis_date='2025-07-12',
        save_results=True
    )
    
    print(f"\n测试完成!")
    for ticker, result in results.items():
        print(f"{ticker}: {result.status}")
        if result.status == "completed":
            print(f"  处理时间: {result.total_processing_time:.1f}秒")
            print(f"  最终决策: {result.final_decision[:100] if result.final_decision else 'None'}...")
        elif result.status == "error":
            print(f"  错误: {result.error_message}")

if __name__ == "__main__":
    test_basic()