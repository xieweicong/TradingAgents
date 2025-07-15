from ddgs import DDGS
import json

def get_fundamentals_deepseek(ticker: str, curr_date: str) -> str:
    """DeepSeek-compatible replacement using ddgs"""
    try:
        ddgs = DDGS()
        
        # Simple targeted search
        results = ddgs.text(f"{ticker} PE ratio revenue debt analysis", max_results=4)
        
        if not results:
            return fallback_manual_report(ticker)
        
        # Build concise report
        content_parts = []
        for i, result in enumerate(results[:4], 1):
            title = result.get('title', 'No title')
            body = result.get('body', '')[:150]
            content_parts.append(f"{i}. {title}\n{body}...")
        
        content = '\n\n'.join(content_parts)
        
        return f"# {ticker} Fundamental Overview ({curr_date})\n\n## Web Insights:\n{content}\n\n## Manual Verification Required:\n- SEC: https://sec.gov/edgar\n- Yahoo: https://finance.yahoo.com/quote/{ticker}"
        
    except Exception:
        return fallback_manual_report(ticker)


def fallback_manual_report(ticker: str) -> str:
    return f"# {ticker} Fundamental Analysis\n\nDue to search limitations, please verify manually:\n\n## Key Actions:\n1. Check Yahoo Finance for {ticker}\n2. Review latest SEC filings\n3. Visit company investor relations\n\n## Metrics to Verify:\n- PE Ratio\n- Revenue Growth\n- Cash Flow\n\nSources: SEC.gov, Yahoo Finance, Company Reports"