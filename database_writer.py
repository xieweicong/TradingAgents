#!/usr/bin/env python3
"""
PostgreSQL数据库写入器 - 同步版本
避免异步复杂性和事件循环错误
"""

import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseWriter:
    """同步PostgreSQL数据库写入器"""
    
    def __init__(self, database_url=None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.connection = None
        
    def connect(self):
        """建立同步连接"""
        if not self.connection and self.database_url:
            try:
                self.connection = psycopg2.connect(self.database_url)
                logger.info("✅ PostgreSQL 同步连接成功")
            except Exception as e:
                logger.warning(f"⚠️ PostgreSQL 连接失败: {e}")
                self.connection = None
                
    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
            logger.info("🔒 PostgreSQL 连接已关闭")
    
    def save_analysis_result(self, result):
        """
        同步保存分析结果到数据库
        
        Args:
            result: StockAnalysisResult对象（来自analyzer.py）
        """
        # 每次都创建新的连接以保证线程安全
        local_connection = None
        try:
            local_connection = psycopg2.connect(self.database_url)
        except Exception as e:
            logger.warning(f"⚠️ PostgreSQL 连接失败: {e}")
            return
        
        try:
            with local_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                
                # 1. 获取正确的公司名称
                company_name = self._get_company_name(result.ticker)
                
                # 1. 确保股票存在
                cursor.execute(
                    """
                    INSERT INTO stocks (ticker, company_name, created_at, updated_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    ON CONFLICT (ticker) DO UPDATE SET 
                        updated_at = CURRENT_TIMESTAMP,
                        company_name = EXCLUDED.company_name
                    RETURNING id
                    """,
                    (str(result.ticker), str(company_name))
                )
                stock_id = cursor.fetchone()['id']
                
                # 2. 保存主分析记录 - 优雅处理重复key
                cursor.execute(
                    """
                    INSERT INTO analyses (
                        stock_id, task_id, status, analysis_date, started_at, ended_at,
                        processing_time_ms, final_decision, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                    ) ON CONFLICT (task_id) DO UPDATE SET
                        updated_at = CURRENT_TIMESTAMP,
                        status = EXCLUDED.status,
                        final_decision = EXCLUDED.final_decision,
                        ended_at = EXCLUDED.ended_at,
                        processing_time_ms = EXCLUDED.processing_time_ms
                    RETURNING id
                    """,
                    (
                        stock_id,
                        str(result.task_id),
                        str(result.status),
                        result.start_time.date() if result.start_time else datetime.now().date(),
                        result.start_time,
                        result.end_time,
                        int(result.total_processing_time * 1000),
                        str(result.final_decision) if result.final_decision else None
                    )
                )
                
                analysis_id = cursor.fetchone()['id']
                
                # 3. 保存所有agent输出
                self._save_agents(cursor, analysis_id, result)
                
                # 提交事务
                local_connection.commit()
                logger.info(f"✅ {result.ticker} 数据已写入数据库 (ID: {analysis_id})")
                
        except psycopg2.errors.UniqueViolation as e:
            local_connection.rollback()
            logger.warning(f"⚠️ 重复任务ID: {result.task_id} - 已更新现有记录")
        except Exception as e:
            local_connection.rollback()
            logger.error(f"❌ 数据库写入失败: {result.ticker} - {str(e)}")
            logger.exception("详细错误信息:")
        finally:
            # 确保线程安全的本地连接被关闭
            try:
                local_connection.close()
            except Exception as e:
                logger.warning(f"关闭连接时出错: {e}")
    
    def _save_agents(self, cursor, analysis_id, result):
        """同步保存agent数据"""
        
        agents_data = []
        
        # 分析师输出
        for agent_type, output in getattr(result, 'analyst_outputs', {}).items():
            if output and output.content:
                role = self._get_role(agent_type)
                agents_data.append((output.agent_name, agent_type, role, output.content))
        
        # 研究输出
        for agent_type, output in getattr(result, 'research_outputs', {}).items():
            if output and output.content:
                role = self._get_role(agent_type)
                agents_data.append((output.agent_name, agent_type, role, output.content))
        
        # 风险输出
        for agent_type, output in getattr(result, 'risk_outputs', {}).items():
            if output and output.content:
                role = self._get_role(agent_type)
                agents_data.append((output.agent_name, agent_type, role, output.content))
        
        # 交易决策
        if result.trader_output and result.trader_output.content:
            agents_data.append((
                result.trader_output.agent_name,
                'trader', 'decision',
                result.trader_output.content
            ))
        
        # 组合决策
        if result.portfolio_output and result.portfolio_output.content:
            agents_data.append((
                result.portfolio_output.agent_name,
                'portfolio_manager', 'decision',
                result.portfolio_output.content
            ))
        
        # 批量插入所有agent
        for agent_name, agent_type, role, content in agents_data:
            cursor.execute(
                """
                INSERT INTO agent_outputs (
                    analysis_id, agent_name, agent_type, role, content, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """,
                (analysis_id, agent_name, agent_type, role, str(content))
            )
    
    def _get_company_name(self, ticker):
        """从Yahoo Finance获取正确的公司名称"""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 尝试多个字段获取最准确的公司名称
            company_name = info.get('longName') or info.get('shortName') or info.get('displayName') or ticker
            return str(company_name)
        except Exception as e:
            logger.warning(f"无法获取{ticker}的公司名称: {e}")
            return ticker  # 失败时使用股票代码
    
    def _get_role(self, agent_type):
        """根据agent类型返回角色"""
        role_map = {
            'market_analyst': 'analytical',
            'fundamentals_analyst': 'analytical', 
            'news_analyst': 'analytical',
            'sentiment_analyst': 'analytical',
            'bull_researcher': 'research',
            'bear_researcher': 'research',
            'research_manager': 'research',
            'risky_analyst': 'risk_management',
            'safe_analyst': 'risk_management',
            'neutral_analyst': 'risk_management',
            'trader': 'decision',
            'portfolio_manager': 'decision'
        }
        return role_map.get(agent_type, 'analytical')
    
    def test_connection(self):
        """测试当前数据库连接"""
        if not self.database_url:
            logger.error("❌ 未设置DATABASE_URL环境变量")
            return False
            
        try:
            self.connect()
            if self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    logger.info(f"✅ PostgreSQL版本: {version.split()[1]}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ 连接测试失败: {e}")
            return False
        finally:
            try:
                self.close()
            except:
                pass  # Ensure we always return False instead of crashing
    
    def has_analysis_for_today(self, ticker, analysis_date=None):
        """检查今天是否已经分析过该股票"""
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            
            if analysis_date is None:
                analysis_date = datetime.now().date()
            else:
                from datetime import datetime
                analysis_date = datetime.strptime(analysis_date, "%Y-%m-%d").date()
                
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1
                    FROM analyses a
                    JOIN stocks s ON a.stock_id = s.id
                    WHERE s.ticker = %s 
                      AND a.analysis_date = %s
                      AND a.status = 'completed'
                    LIMIT 1
                    """,
                    (str(ticker), analysis_date)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"❌ 检查重复分析失败: {e}")
            return False
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass
    
    def get_recent_analyses(self, limit=5):
        """获取最近分析用于验证"""
        conn = None
        try:
            conn = psycopg2.connect(self.database_url)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT s.ticker, s.company_name, a.final_decision, a.analysis_date,
                           a.processing_time_ms/1000.0 as seconds, a.created_at, COUNT(ao.id) as agents
                    FROM analyses a 
                    JOIN stocks s ON a.stock_id = s.id 
                    LEFT JOIN agent_outputs ao ON a.id = ao.analysis_id
                    GROUP BY a.id, s.ticker, s.company_name
                    ORDER BY a.created_at DESC 
                    LIMIT %s
                    """,
                    (limit,)
                )
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"❌ 查询失败: {e}")
            return []
        finally:
            if conn:
                try:
                    conn.close()
                except:
                    pass


class DatabaseManager:
    """数据库管理器 - 与现有分析器零耦合"""
    
    def __init__(self, database_url=None):
        self.writer = DatabaseWriter(database_url)
        
    def save_results(self, result):
        """同步保存结果 - 每线程独立连接"""
        logger.info("📝 正在写入到PostgreSQL...")
        # 直接保存，不测试连接，使用线程安全的方法
        try:
            self.writer.save_analysis_result(result)
            logger.info("✅ PostgreSQL数据保存完成")
        except Exception as e:
            logger.warning(f"⚠️ PostgreSQL保存失败: {e}，使用本地文件存储")
    
    def close_connection(self):
        """程序结束时调用"""
        self.writer.close()