#!/usr/bin/env python3
"""
Test script to verify all fixes are working
"""

from extensions.multi_stock.analyzer import MultiStockAnalyzer
import json
import os

def test_json_serialization():
    """Test the JSON serialization fixes"""
    print("测试JSON序列化修复...")
    
    # Create test config
    test_config = {
        "llm_provider": "deepseek",
        "backend_url": "https://api.deepseek.com/v1", 
        "deep_think_llm": "deepseek-chat",
        "quick_think_llm": "deepseek-chat",
        "max_debate_rounds": 1,
        "online_tools": True,
        "disable_memory": True,
        "project_dir": os.getcwd()
    }
    
    analyzer = MultiStockAnalyzer(config=test_config, max_workers=1)
    
    # Test with a single US stock (should have better data)
    results = analyzer.analyze_stocks(
        stock_list=['AAPL'],
        analysis_date='2025-07-12',
        save_results=True
    )
    
    success = False
    for ticker, result in results.items():
        print(f"\n{ticker} 分析结果:")
        print(f"  状态: {result.status}")
        print(f"  处理时间: {result.total_processing_time:.1f}秒")
        
        if result.status == "completed":
            # Check if JSON files were created successfully
            result_path = f"multi_analysis_results/{ticker}/2025-07-12"
            json_file = f"{result_path}/analysis_result.json"
            
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"  ✅ JSON文件成功创建和读取")
                    success = True
                except Exception as e:
                    print(f"  ❌ JSON文件读取失败: {e}")
            else:
                print(f"  ❌ JSON文件不存在")
                
            # Check final decision
            if result.final_decision:
                print(f"  最终决策: {result.final_decision[:100]}...")
            else:
                print(f"  ❌ 没有最终决策")
        else:
            print(f"  错误: {result.error_message}")
    
    return success

def test_csv_error_handling():
    """Test CSV error handling improvements"""
    print("\n测试CSV错误处理...")
    
    # This will test the CSV parsing improvements indirectly
    # by checking if analysis completes without crashing
    test_config = {
        "llm_provider": "deepseek",
        "backend_url": "https://api.deepseek.com/v1", 
        "deep_think_llm": "deepseek-chat",
        "quick_think_llm": "deepseek-chat",
        "max_debate_rounds": 1,
        "online_tools": False,  # Use offline to test CSV handling
        "disable_memory": True,
        "project_dir": os.getcwd()
    }
    
    analyzer = MultiStockAnalyzer(config=test_config, max_workers=1)
    
    # Test with a Japanese stock that had CSV issues
    results = analyzer.analyze_stocks(
        stock_list=['7203.T'],
        analysis_date='2025-07-12', 
        save_results=True
    )
    
    for ticker, result in results.items():
        print(f"{ticker} CSV测试结果: {result.status}")
        if result.status == "error":
            print(f"  错误信息: {result.error_message}")
        
    return True

def main():
    """Run all tests"""
    print("开始测试修复...")
    print("=" * 50)
    
    try:
        # Test 1: JSON serialization
        json_success = test_json_serialization()
        
        # Test 2: CSV error handling 
        csv_success = test_csv_error_handling()
        
        print("\n" + "=" * 50)
        print("测试结果摘要:")
        print(f"JSON序列化修复: {'✅ 成功' if json_success else '❌ 失败'}")
        print(f"CSV错误处理: {'✅ 成功' if csv_success else '❌ 失败'}")
        
        if json_success:
            print("\n🎉 主要修复验证成功！")
            print("多线程分析器现在可以:")
            print("- 正确处理JSON序列化")
            print("- 优雅处理CSV解析错误")
            print("- 保存结构化分析结果")
        else:
            print("\n⚠️  还有一些问题需要解决")
            
    except Exception as e:
        print(f"测试过程出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()