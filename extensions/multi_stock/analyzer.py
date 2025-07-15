#!/usr/bin/env python3
"""
Multi-Stock Trading Agents Analyzer

A multi-threaded analysis framework that:
1. Analyzes multiple stocks concurrently using API calls
2. Categorizes and saves different agents' outputs
3. Structures data for future database integration
4. Provides easy stock list management

Usage:
    python multi_stock_analyzer.py
"""

import os
import sys
import json
import asyncio
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path
import time
import traceback

from dotenv import load_dotenv
load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG


@dataclass
class AnalysisTask:
    """Represents a single stock analysis task"""
    ticker: str
    analysis_date: str
    config: Dict[str, Any]
    task_id: str = None
    
    def __post_init__(self):
        if self.task_id is None:
            self.task_id = f"{self.ticker}_{self.analysis_date}_{int(time.time())}"


@dataclass
class AgentOutput:
    """Structure for individual agent output"""
    agent_type: str  # e.g., "market_analyst", "news_analyst", etc.
    agent_name: str  # e.g., "Market Analyst", "News Analyst", etc.
    content: str
    timestamp: datetime
    processing_time: float = 0.0
    status: str = "completed"  # completed, error, timeout
    error_message: Optional[str] = None


@dataclass
class StockAnalysisResult:
    """Complete analysis result for a single stock"""
    ticker: str
    analysis_date: str
    task_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_processing_time: float = 0.0
    status: str = "running"  # running, completed, error
    
    # Agent outputs categorized by team
    analyst_outputs: Dict[str, AgentOutput] = None
    research_outputs: Dict[str, AgentOutput] = None  
    trader_output: Optional[AgentOutput] = None
    risk_outputs: Dict[str, AgentOutput] = None
    portfolio_output: Optional[AgentOutput] = None
    
    # Final decision and raw state
    final_decision: Optional[str] = None
    raw_state: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.analyst_outputs is None:
            self.analyst_outputs = {}
        if self.research_outputs is None:
            self.research_outputs = {}
        if self.risk_outputs is None:
            self.risk_outputs = {}


class StockListManager:
    """Manages the list of stocks to analyze"""
    
    def __init__(self, stock_list_file: str = "stock_list.json"):
        self.stock_list_file = stock_list_file
        self.load_stock_list()
    
    def load_stock_list(self):
        """Load stock list from file or create default"""
        if os.path.exists(self.stock_list_file):
            with open(self.stock_list_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.stock_lists = data.get('stock_lists', {})
                self.default_list = data.get('default_list', 'us_stocks')
        else:
            # Create default stock lists
            self.stock_lists = {
                'us_stocks': ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'AMZN'],
                'jp_stocks': ['7203.T', '6758.T', '9984.T', '6861.T', '8316.T'],
                'test_stocks': ['AAPL', 'NVDA'],
                'custom': []
            }
            self.default_list = 'test_stocks'
            self.save_stock_list()
    
    def save_stock_list(self):
        """Save stock list to file"""
        data = {
            'stock_lists': self.stock_lists,
            'default_list': self.default_list
        }
        with open(self.stock_list_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_stock_list(self, list_name: str = None) -> List[str]:
        """Get stocks from specified list or default"""
        if list_name is None:
            list_name = self.default_list
        return self.stock_lists.get(list_name, [])
    
    def add_stock_list(self, list_name: str, stocks: List[str]):
        """Add a new stock list"""
        self.stock_lists[list_name] = stocks
        self.save_stock_list()
    
    def add_stock_to_list(self, list_name: str, ticker: str):
        """Add a stock to existing list"""
        if list_name in self.stock_lists:
            if ticker not in self.stock_lists[list_name]:
                self.stock_lists[list_name].append(ticker)
                self.save_stock_list()
    
    def remove_stock_from_list(self, list_name: str, ticker: str):
        """Remove a stock from existing list"""
        if list_name in self.stock_lists and ticker in self.stock_lists[list_name]:
            self.stock_lists[list_name].remove(ticker)
            self.save_stock_list()
    
    def list_available_lists(self) -> Dict[str, List[str]]:
        """Return all available stock lists"""
        return self.stock_lists.copy()


class ResultsManager:
    """Manages storage and retrieval of analysis results"""
    
    def __init__(self, base_dir: str = "multi_analysis_results"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        # 可选：添加同步数据库写入器
        try:
            from database_writer import DatabaseManager
            self.db_manager = DatabaseManager()
        except ImportError:
            self.db_manager = None
    
    def get_storage_path(self, ticker: str, analysis_date: str) -> Path:
        """Get storage path for a specific analysis"""
        return self.base_dir / ticker / analysis_date
    
    def save_analysis_result(self, result: StockAnalysisResult):
        """Save complete analysis result to structured files"""
        storage_path = self.get_storage_path(result.ticker, result.analysis_date)
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Save main result as JSON (for database preparation)
        result_dict = asdict(result)
        
        # Clean up raw_state to remove non-serializable objects
        if result_dict.get('raw_state'):
            result_dict['raw_state'] = self._clean_raw_state(result_dict['raw_state'])
        
        # Convert datetime objects to strings for JSON serialization
        if result_dict['start_time']:
            result_dict['start_time'] = result_dict['start_time'].isoformat()
        if result_dict['end_time']:
            result_dict['end_time'] = result_dict['end_time'].isoformat()
        
        # Convert agent output timestamps
        for category in ['analyst_outputs', 'research_outputs', 'risk_outputs']:
            if result_dict[category]:
                for agent_key, agent_output in result_dict[category].items():
                    if agent_output and 'timestamp' in agent_output:
                        agent_output['timestamp'] = agent_output['timestamp'].isoformat()
        
        if result_dict['trader_output'] and 'timestamp' in result_dict['trader_output']:
            result_dict['trader_output']['timestamp'] = result_dict['trader_output']['timestamp'].isoformat()
        if result_dict['portfolio_output'] and 'timestamp' in result_dict['portfolio_output']:
            result_dict['portfolio_output']['timestamp'] = result_dict['portfolio_output']['timestamp'].isoformat()
        
        # Save structured result
        try:
            with open(storage_path / "analysis_result.json", 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            # If JSON serialization fails, save a simplified version
            simplified_result = self._create_simplified_result(result)
            with open(storage_path / "analysis_result.json", 'w', encoding='utf-8') as f:
                json.dump(simplified_result, f, indent=2, ensure_ascii=False)
        
        # 同步写入数据库（解决async问题）
        if self.db_manager:
            print(f"📝 正在写入 {result.ticker} 到 PostgreSQL...")
            try:
                self.db_manager.save_results(result)
                print(f"✅ {result.ticker} 数据已成功写入 PostgreSQL")
            except Exception as e:
                print(f"⚠️ {result.ticker} 数据库写入失败: {str(e)}")
                print(f"   继续本地文件存储...")
                logging.warning(f"PostgreSQL write failed for {result.ticker}: {e}")
        
        # Save individual agent outputs as separate files (for easy access)
        self._save_agent_outputs(storage_path, result)
        
        # Save final decision
        if result.final_decision:
            with open(storage_path / "final_decision.txt", 'w', encoding='utf-8') as f:
                f.write(result.final_decision)
        
        # Save raw state for debugging (cleaned version)
        if result.raw_state:
            try:
                cleaned_raw_state = self._clean_raw_state(result.raw_state)
                with open(storage_path / "raw_state.json", 'w', encoding='utf-8') as f:
                    json.dump(cleaned_raw_state, f, indent=2, ensure_ascii=False)
            except Exception as e:
                # Save error info if raw state can't be serialized
                with open(storage_path / "raw_state_error.txt", 'w', encoding='utf-8') as f:
                    f.write(f"Raw state serialization failed: {str(e)}\n")
                    f.write(f"Raw state type: {type(result.raw_state)}\n")
                    if hasattr(result.raw_state, 'keys'):
                        f.write(f"Raw state keys: {list(result.raw_state.keys())}")
    
    def _save_agent_outputs(self, storage_path: Path, result: StockAnalysisResult):
        """Save individual agent outputs to separate files"""
        # Create agent directories
        agents_dir = storage_path / "agents"
        agents_dir.mkdir(exist_ok=True)
        
        # Save analyst outputs
        if result.analyst_outputs:
            analyst_dir = agents_dir / "analysts"
            analyst_dir.mkdir(exist_ok=True)
            for agent_type, output in result.analyst_outputs.items():
                if output and output.content:
                    with open(analyst_dir / f"{agent_type}.md", 'w', encoding='utf-8') as f:
                        f.write(f"# {output.agent_name}\n\n")
                        f.write(f"**Analysis Date:** {result.analysis_date}\n")
                        f.write(f"**Timestamp:** {output.timestamp}\n")
                        f.write(f"**Processing Time:** {output.processing_time:.2f}s\n")
                        f.write(f"**Status:** {output.status}\n\n")
                        f.write("---\n\n")
                        f.write(output.content)
        
        # Save research outputs  
        if result.research_outputs:
            research_dir = agents_dir / "research"
            research_dir.mkdir(exist_ok=True)
            for agent_type, output in result.research_outputs.items():
                if output and output.content:
                    with open(research_dir / f"{agent_type}.md", 'w', encoding='utf-8') as f:
                        f.write(f"# {output.agent_name}\n\n")
                        f.write(f"**Analysis Date:** {result.analysis_date}\n")
                        f.write(f"**Timestamp:** {output.timestamp}\n")
                        f.write(f"**Processing Time:** {output.processing_time:.2f}s\n")
                        f.write(f"**Status:** {output.status}\n\n")
                        f.write("---\n\n")
                        f.write(output.content)
        
        # Save trader output
        if result.trader_output and result.trader_output.content:
            trader_dir = agents_dir / "trader"
            trader_dir.mkdir(exist_ok=True)
            with open(trader_dir / "trader_plan.md", 'w', encoding='utf-8') as f:
                f.write(f"# {result.trader_output.agent_name}\n\n")
                f.write(f"**Analysis Date:** {result.analysis_date}\n")
                f.write(f"**Timestamp:** {result.trader_output.timestamp}\n")
                f.write(f"**Processing Time:** {result.trader_output.processing_time:.2f}s\n")
                f.write(f"**Status:** {result.trader_output.status}\n\n")
                f.write("---\n\n")
                f.write(result.trader_output.content)
        
        # Save risk outputs
        if result.risk_outputs:
            risk_dir = agents_dir / "risk_management"
            risk_dir.mkdir(exist_ok=True)
            for agent_type, output in result.risk_outputs.items():
                if output and output.content:
                    with open(risk_dir / f"{agent_type}.md", 'w', encoding='utf-8') as f:
                        f.write(f"# {output.agent_name}\n\n")
                        f.write(f"**Analysis Date:** {result.analysis_date}\n")
                        f.write(f"**Timestamp:** {output.timestamp}\n")
                        f.write(f"**Processing Time:** {output.processing_time:.2f}s\n")
                        f.write(f"**Status:** {output.status}\n\n")
                        f.write("---\n\n")
                        f.write(output.content)
        
        # Save portfolio output
        if result.portfolio_output and result.portfolio_output.content:
            portfolio_dir = agents_dir / "portfolio"
            portfolio_dir.mkdir(exist_ok=True)
            with open(portfolio_dir / "portfolio_decision.md", 'w', encoding='utf-8') as f:
                f.write(f"# {result.portfolio_output.agent_name}\n\n")
                f.write(f"**Analysis Date:** {result.analysis_date}\n")
                f.write(f"**Timestamp:** {result.portfolio_output.timestamp}\n")
                f.write(f"**Processing Time:** {result.portfolio_output.processing_time:.2f}s\n")
                f.write(f"**Status:** {result.portfolio_output.status}\n\n")
                f.write("---\n\n")
                f.write(result.portfolio_output.content)
    
    def _clean_raw_state(self, raw_state):
        """Clean raw state to remove non-serializable objects"""
        if not isinstance(raw_state, dict):
            return str(raw_state)
        
        cleaned = {}
        for key, value in raw_state.items():
            try:
                if key == 'messages':
                    # Handle message objects specially
                    cleaned[key] = self._clean_messages(value)
                elif hasattr(value, '__dict__'):
                    # Convert objects to strings
                    cleaned[key] = str(value)
                elif isinstance(value, (dict, list)):
                    # Recursively clean nested structures
                    cleaned[key] = self._clean_nested_structure(value)
                else:
                    # Keep primitive types
                    cleaned[key] = value
            except Exception:
                # If anything fails, convert to string
                cleaned[key] = str(value)
        
        return cleaned
    
    def _clean_messages(self, messages):
        """Clean message objects to extract text content"""
        if not isinstance(messages, list):
            return str(messages)
        
        cleaned_messages = []
        for msg in messages:
            try:
                if hasattr(msg, 'content'):
                    cleaned_messages.append({
                        'type': type(msg).__name__,
                        'content': str(msg.content)
                    })
                else:
                    cleaned_messages.append(str(msg))
            except Exception:
                cleaned_messages.append(str(msg))
        
        return cleaned_messages
    
    def _clean_nested_structure(self, obj):
        """Recursively clean nested dictionaries and lists"""
        try:
            if isinstance(obj, dict):
                return {k: self._clean_nested_structure(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [self._clean_nested_structure(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return str(obj)
            else:
                return obj
        except Exception:
            return str(obj)
    
    def _create_simplified_result(self, result: StockAnalysisResult):
        """Create a simplified result that can be JSON serialized"""
        return {
            'ticker': result.ticker,
            'analysis_date': result.analysis_date,
            'task_id': result.task_id,
            'start_time': result.start_time.isoformat() if result.start_time else None,
            'end_time': result.end_time.isoformat() if result.end_time else None,
            'total_processing_time': result.total_processing_time,
            'status': result.status,
            'final_decision': result.final_decision,
            'error_message': result.error_message,
            'analyst_outputs_count': len(result.analyst_outputs) if result.analyst_outputs else 0,
            'research_outputs_count': len(result.research_outputs) if result.research_outputs else 0,
            'has_trader_output': result.trader_output is not None,
            'risk_outputs_count': len(result.risk_outputs) if result.risk_outputs else 0,
            'has_portfolio_output': result.portfolio_output is not None,
            'serialization_note': 'Simplified version due to serialization issues'
        }


class SingleStockAnalyzer:
    """Handles analysis of a single stock"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def analyze_stock(self, task: AnalysisTask) -> StockAnalysisResult:
        """Analyze a single stock and return structured results"""
        result = StockAnalysisResult(
            ticker=task.ticker,
            analysis_date=task.analysis_date,
            task_id=task.task_id,
            start_time=datetime.now()
        )
        
        try:
            print(f"开始分析 {task.ticker} ({task.analysis_date})")
            
            # Create unique config for this task to avoid memory collection conflicts
            unique_config = task.config.copy()
            # Add unique identifier to prevent ChromaDB collection name conflicts
            import uuid
            import threading
            unique_id = f"{threading.current_thread().ident}_{str(uuid.uuid4())[:8]}"
            unique_config["memory_suffix"] = f"_{task.ticker}_{unique_id}"
            
            # Initialize the trading graph
            ta = TradingAgentsGraph(debug=False, config=unique_config)
            
            # Run the analysis
            final_state, decision = ta.propagate(task.ticker, task.analysis_date)
            
            # Extract and categorize agent outputs
            result = self._extract_agent_outputs(result, final_state)
            result.final_decision = str(decision) if decision else None
            result.raw_state = final_state
            result.status = "completed"
            
            print(f"完成分析 {task.ticker}")
            
        except Exception as e:
            result.status = "error"
            result.error_message = str(e)
            print(f"分析失败 {task.ticker}: {str(e)}")
            traceback.print_exc()
        
        finally:
            result.end_time = datetime.now()
            result.total_processing_time = (result.end_time - result.start_time).total_seconds()
        
        return result
    
    def _extract_agent_outputs(self, result: StockAnalysisResult, final_state: Dict[str, Any]) -> StockAnalysisResult:
        """Extract and categorize agent outputs from final state"""
        timestamp = datetime.now()
        
        # Extract analyst outputs
        analyst_mappings = {
            'market_report': ('market_analyst', 'Market Analyst'),
            'sentiment_report': ('sentiment_analyst', 'Sentiment Analyst'),
            'news_report': ('news_analyst', 'News Analyst'),
            'fundamentals_report': ('fundamentals_analyst', 'Fundamentals Analyst')
        }
        
        for state_key, (agent_type, agent_name) in analyst_mappings.items():
            if state_key in final_state and final_state[state_key]:
                result.analyst_outputs[agent_type] = AgentOutput(
                    agent_type=agent_type,
                    agent_name=agent_name,
                    content=final_state[state_key],
                    timestamp=timestamp
                )
        
        # Extract research outputs
        if 'investment_debate_state' in final_state and final_state['investment_debate_state']:
            debate_state = final_state['investment_debate_state']
            
            if 'bull_history' in debate_state and debate_state['bull_history']:
                result.research_outputs['bull_researcher'] = AgentOutput(
                    agent_type='bull_researcher',
                    agent_name='Bull Researcher',
                    content=debate_state['bull_history'],
                    timestamp=timestamp
                )
            
            if 'bear_history' in debate_state and debate_state['bear_history']:
                result.research_outputs['bear_researcher'] = AgentOutput(
                    agent_type='bear_researcher',
                    agent_name='Bear Researcher',
                    content=debate_state['bear_history'],
                    timestamp=timestamp
                )
            
            if 'judge_decision' in debate_state and debate_state['judge_decision']:
                result.research_outputs['research_manager'] = AgentOutput(
                    agent_type='research_manager',
                    agent_name='Research Manager',
                    content=debate_state['judge_decision'],
                    timestamp=timestamp
                )
        
        # Extract trader output
        if 'trader_investment_plan' in final_state and final_state['trader_investment_plan']:
            result.trader_output = AgentOutput(
                agent_type='trader',
                agent_name='Trader',
                content=final_state['trader_investment_plan'],
                timestamp=timestamp
            )
        
        # Extract risk management outputs
        if 'risk_debate_state' in final_state and final_state['risk_debate_state']:
            risk_state = final_state['risk_debate_state']
            
            risk_mappings = {
                'risky_history': ('risky_analyst', 'Aggressive Analyst'),
                'safe_history': ('safe_analyst', 'Conservative Analyst'),
                'neutral_history': ('neutral_analyst', 'Neutral Analyst')
            }
            
            for state_key, (agent_type, agent_name) in risk_mappings.items():
                if state_key in risk_state and risk_state[state_key]:
                    result.risk_outputs[agent_type] = AgentOutput(
                        agent_type=agent_type,
                        agent_name=agent_name,
                        content=risk_state[state_key],
                        timestamp=timestamp
                    )
            
            # Portfolio manager decision
            if 'judge_decision' in risk_state and risk_state['judge_decision']:
                result.portfolio_output = AgentOutput(
                    agent_type='portfolio_manager',
                    agent_name='Portfolio Manager',
                    content=risk_state['judge_decision'],
                    timestamp=timestamp
                )
        
        return result


class LogManager:
    """Centralized logging manager for multi-stock analysis"""
    
    def __init__(self, log_dir: str = "multi_analysis_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Main log file
        log_file = self.log_dir / f"analysis_session_{self.session_id}.log"
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # Setup main logger
        self.logger = logging.getLogger('MultiStockAnalyzer')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def log_analysis_start(self, ticker: str, analysis_date: str):
        """Log start of stock analysis"""
        self.logger.info(f"开始分析股票: {ticker} (日期: {analysis_date})")
    
    def log_analysis_complete(self, ticker: str, processing_time: float, status: str):
        """Log completion of stock analysis"""
        self.logger.info(f"完成分析股票: {ticker} (用时: {processing_time:.2f}s, 状态: {status})")
    
    def log_analysis_error(self, ticker: str, error: str):
        """Log analysis error"""
        self.logger.error(f"分析失败 {ticker}: {error}")
    
    def log_progress_update(self, status: Dict[str, int]):
        """Log progress update"""
        self.logger.info(
            f"进度更新 - 总计: {status['total']}, "
            f"等待: {status['pending']}, "
            f"运行中: {status['running']}, "
            f"完成: {status['completed']}, "
            f"失败: {status['failed']}"
        )
    
    def log_session_summary(self, results: Dict[str, Any]):
        """Log session summary"""
        total = len(results)
        completed = sum(1 for r in results.values() if r.status == "completed")
        failed = total - completed
        
        self.logger.info(f"分析会话完成 - 总股票数: {total}, 成功: {completed}, 失败: {failed}")
        
        # Create summary file
        summary_file = self.log_dir / f"session_summary_{self.session_id}.json"
        summary_data = {
            "session_id": self.session_id,
            "total_stocks": total,
            "completed": completed,
            "failed": failed,
            "results": {
                ticker: {
                    "status": result.status,
                    "processing_time": result.total_processing_time,
                    "error_message": result.error_message
                }
                for ticker, result in results.items()
            }
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    def create_stock_logger(self, ticker: str) -> logging.Logger:
        """Create dedicated logger for individual stock analysis"""
        stock_logger = logging.getLogger(f'Stock_{ticker}')
        stock_logger.setLevel(logging.DEBUG)
        
        # Create stock-specific log file
        stock_log_file = self.log_dir / f"stock_{ticker}_{self.session_id}.log"
        
        stock_handler = logging.FileHandler(stock_log_file, encoding='utf-8')
        stock_handler.setLevel(logging.DEBUG)
        stock_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        
        stock_logger.addHandler(stock_handler)
        stock_logger.propagate = False
        
        return stock_logger


class ProgressTracker:
    """Tracks progress of multiple stock analyses"""
    
    def __init__(self):
        self.tasks = {}
        self.completed = {}
        self.failed = {}
        self.lock = threading.Lock()
    
    def add_task(self, task: AnalysisTask):
        with self.lock:
            self.tasks[task.task_id] = {
                'task': task,
                'status': 'pending',
                'start_time': None,
                'end_time': None
            }
    
    def start_task(self, task_id: str):
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'running'
                self.tasks[task_id]['start_time'] = datetime.now()
    
    def complete_task(self, task_id: str, result: StockAnalysisResult):
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'completed'
                self.tasks[task_id]['end_time'] = datetime.now()
                self.completed[task_id] = result
    
    def fail_task(self, task_id: str, error: str):
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['end_time'] = datetime.now()
                self.failed[task_id] = error
    
    def get_status(self):
        with self.lock:
            total = len(self.tasks)
            running = sum(1 for t in self.tasks.values() if t['status'] == 'running')
            completed = sum(1 for t in self.tasks.values() if t['status'] == 'completed')
            failed = sum(1 for t in self.tasks.values() if t['status'] == 'failed')
            pending = total - running - completed - failed
            
            return {
                'total': total,
                'pending': pending,
                'running': running,
                'completed': completed,
                'failed': failed
            }
    
    def print_status(self):
        status = self.get_status()
        print(f"\n进度状态: 总计={status['total']}, 等待={status['pending']}, 运行中={status['running']}, 完成={status['completed']}, 失败={status['failed']}")


class MultiStockAnalyzer:
    """Multi-threaded stock analysis manager"""
    
    def __init__(self, config: Dict[str, Any] = None, max_workers: int = 4):
        self.config = config or self._get_default_config()
        self.max_workers = max_workers
        self.stock_manager = StockListManager()
        self.results_manager = ResultsManager()
        self.progress_tracker = ProgressTracker()
        self.log_manager = LogManager()
        self._memory_lock = threading.Lock()  # Lock for memory operations
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = "deepseek"
        config["backend_url"] = "https://api.deepseek.com/v1"
        config["deep_think_llm"] = "deepseek-reasoner"
        config["quick_think_llm"] = "deepseek-chat"
        config["max_debate_rounds"] = 1
        config["online_tools"] = True
        config["disable_memory"] = True  # Disable memory to avoid conflicts
        config["project_dir"] = os.getcwd()  # Set project directory to current directory
        return config
    
    def analyze_stocks(self, 
                      stock_list: List[str] = None,
                      stock_list_name: str = None,
                      analysis_date: str = None,
                      save_results: bool = True,
                      skip_existing: bool = True) -> Dict[str, StockAnalysisResult]:
        """Analyze multiple stocks concurrently"""
        
        # Clean up any existing memory collections first
        self._cleanup_memory_collections()
        
        # Determine which stocks to analyze
        if stock_list is None:
            stock_list = self.stock_manager.get_stock_list(stock_list_name)
        
        if not stock_list:
            raise ValueError("No stocks specified for analysis")
        
        # Determine analysis date
        if analysis_date is None:
            analysis_date = datetime.now().strftime("%Y-%m-%d")
        
        # Log analysis start
        self.log_manager.logger.info(f"开始多股票分析 - 股票列表: {stock_list}")
        self.log_manager.logger.info(f"分析日期: {analysis_date}")
        self.log_manager.logger.info(f"最大并发数: {self.max_workers}")
        self.log_manager.logger.info(f"配置: {self.config['llm_provider']} - {self.config['deep_think_llm']}")
        
        print(f"开始多股票分析")
        print(f"股票列表: {stock_list}")
        print(f"分析日期: {analysis_date}")
        print(f"最大并发数: {self.max_workers}")
        print(f"配置: {self.config['llm_provider']} - {self.config['deep_think_llm']}")
        
        # Create analysis tasks, skip already analyzed ones
        tasks = []
        existing_analyses = {}
        
        # Check existing analyses if skip_existing is enabled
        if skip_existing and self.results_manager.db_manager:
            logger = self.log_manager.logger
            logger.info("正在检查已完成的分析...")
            for ticker in stock_list:
                if self.results_manager.db_manager.writer.has_analysis_for_today(ticker, analysis_date):
                    logger.info(f"跳过 {ticker} - 今日已分析")
                    existing_analyses[ticker] = True
                else:
                    existing_analyses[ticker] = False
        else:
            existing_analyses = {ticker: False for ticker in stock_list}
        
        # Filter stocks to analyze
        stocks_to_analyze = [ticker for ticker in stock_list if not existing_analyses[ticker]]
        
        if not stocks_to_analyze:
            print("所有股票今日已完成分析，跳过本次运行")
            self.log_manager.logger.info("所有股票今日已完成分析，跳过本次运行")
            return {}
            
        print(f"开始分析以下股票: {stocks_to_analyze}")
        self.log_manager.logger.info(f"实际分析股票: {stocks_to_analyze}")
        
        # Create tasks for stocks to analyze
        for ticker in stocks_to_analyze:
            task = AnalysisTask(
                ticker=ticker,
                analysis_date=analysis_date,
                config=self.config.copy()
            )
            tasks.append(task)
            self.progress_tracker.add_task(task)
        
        # Run analyses concurrently
        results = {}
        analyzer = SingleStockAnalyzer(self.config)
        
        def analyze_single_stock(task):
            self.progress_tracker.start_task(task.task_id)
            self.log_manager.log_analysis_start(task.ticker, task.analysis_date)
            
            try:
                result = analyzer.analyze_stock(task)
                
                if result.status == "completed":
                    self.progress_tracker.complete_task(task.task_id, result)
                    self.log_manager.log_analysis_complete(
                        task.ticker, result.total_processing_time, result.status
                    )
                else:
                    self.progress_tracker.fail_task(task.task_id, result.error_message or "Unknown error")
                    self.log_manager.log_analysis_error(
                        task.ticker, result.error_message or "Unknown error"
                    )
                
                return result
            except Exception as e:
                error_msg = str(e)
                self.progress_tracker.fail_task(task.task_id, error_msg)
                self.log_manager.log_analysis_error(task.ticker, error_msg)
                raise
        
        # Start progress monitoring in separate thread
        progress_thread = threading.Thread(target=self._monitor_progress, daemon=True)
        progress_thread.start()
        
        # Execute tasks concurrently with proper exception handling
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(analyze_single_stock, task): task for task in tasks}
            
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result(timeout=600)  # 10 minute timeout
                    results[task.ticker] = result
                    
                    # Save results if requested
                    if save_results:
                        try:
                            self.results_manager.save_analysis_result(result)
                        except Exception as e:
                            print(f"警告：保存{result.ticker}结果时出错: {str(e)}")
                            logging.warning(f"保存{result.ticker}结果失败: {e}")
                        
                except Exception as e:
                    print(f"任务 {task.ticker} 执行失败: {str(e)}")
                    # Create error result but don't crash the system
                    error_result = StockAnalysisResult(
                        ticker=task.ticker,
                        analysis_date=task.analysis_date,
                        task_id=task.task_id,
                        start_time=datetime.now(),
                        end_time=datetime.now(),
                        status="error",
                        error_message=str(e)
                    )
                    results[task.ticker] = error_result
                    # Log but don't raise the exception to prevent terminal kill
                    self.log_manager.logger.error(f"分析任务失败: {task.ticker} - {str(e)}")
        
        # Final status
        self.progress_tracker.print_status()
        print("\n所有分析任务完成!")
        
        # Log session summary
        self.log_manager.log_session_summary(results)
        
        return results
    
    def _monitor_progress(self):
        """Monitor and print progress periodically"""
        last_status = {}
        max_wait_time = 3600  # 60 minutes maximum wait time
        start_time = datetime.now()
        
        while True:
            status = self.progress_tracker.get_status()
            current_time = datetime.now()
            elapsed = (current_time - start_time).total_seconds()
            
            # Break if all tasks are complete or timeout reached
            if status['running'] == 0 and status['pending'] == 0:
                break
            if elapsed > max_wait_time:
                print("⚠️ 进度监控超时 (60分钟)，将停止监控")
                break
            
            # Only log if status changed
            if status != last_status and (status['running'] > 0 or status['completed'] > 0):
                self.progress_tracker.print_status()
                self.log_manager.log_progress_update(status)
                last_status = status.copy()
            
            time.sleep(10)  # Update every 10 seconds
    
    def get_available_stock_lists(self) -> Dict[str, List[str]]:
        """Get all available stock lists"""
        return self.stock_manager.list_available_lists()
    
    def add_stock_list(self, list_name: str, stocks: List[str]):
        """Add a new stock list"""
        self.stock_manager.add_stock_list(list_name, stocks)
    
    def create_custom_config(self, **kwargs) -> Dict[str, Any]:
        """Create custom configuration"""
        config = self.config.copy()
        config.update(kwargs)
        return config
    
    def _cleanup_memory_collections(self):
        """Clean up existing memory collections to prevent conflicts"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            client = chromadb.Client(Settings(allow_reset=True))
            collections = client.list_collections()
            
            for collection in collections:
                if any(name in collection.name for name in ['bull_memory', 'bear_memory']):
                    try:
                        client.delete_collection(collection.name)
                        self.log_manager.logger.debug(f"已清理内存集合: {collection.name}")
                    except:
                        pass
                        
        except Exception as e:
            self.log_manager.logger.warning(f"清理内存集合时出现警告: {str(e)}")


def main():
    """Main function with interactive configuration"""
    print("=" * 60)
    print("Multi-Stock Trading Agents Analyzer")
    print("=" * 60)
    
    # Initialize analyzer with limited workers to avoid memory conflicts
    analyzer = MultiStockAnalyzer(max_workers=1)  # Use 1 worker to avoid ChromaDB conflicts
    
    # Show available stock lists
    available_lists = analyzer.get_available_stock_lists()
    print("\n可用的股票列表:")
    for list_name, stocks in available_lists.items():
        print(f"  {list_name}: {stocks}")
    
    # Get user selections
    print("\n请选择要分析的股票列表:")
    list_name = input("输入列表名 (留空使用默认列表): ").strip()
    if not list_name:
        list_name = None
    
    analysis_date = input(f"输入分析日期 (YYYY-MM-DD, 留空使用今天): ").strip()
    if not analysis_date:
        analysis_date = None
    
    # Run analysis
    try:
        results = analyzer.analyze_stocks(
            stock_list_name=list_name,
            analysis_date=analysis_date,
            save_results=True
        )
        
        # Print summary
        print("\n" + "=" * 60)
        print("分析结果摘要:")
        print("=" * 60)
        
        for ticker, result in results.items():
            status_emoji = "✅" if result.status == "completed" else "❌"
            print(f"{status_emoji} {ticker}: {result.status} (用时: {result.total_processing_time:.1f}s)")
            if result.final_decision:
                print(f"   决策: {result.final_decision[:100]}...")
        
        print(f"\n结果已保存到: multi_analysis_results/")
        
    except Exception as e:
        print(f"分析过程出错: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
