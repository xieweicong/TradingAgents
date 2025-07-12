"""
Enhanced Trading Agents Extensions

This module provides enhanced functionality for the TradingAgents library,
including multi-threading support, API interfaces, and production fixes.

Based on TradingAgents by TauricResearch:
https://github.com/TauricResearch/TradingAgents
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Import enhanced functionality
try:
    from .multi_stock.analyzer import MultiStockAnalyzer
    from .utils.memory_cleanup import cleanup_memory_collections
except ImportError:
    # Graceful degradation if extensions not available
    MultiStockAnalyzer = None

__version__ = "1.0.0"
__author__ = "Enhanced by Community"
__original__ = "TauricResearch"

__all__ = [
    'TradingAgentsGraph',
    'DEFAULT_CONFIG', 
    'MultiStockAnalyzer',
    'cleanup_memory_collections'
]
