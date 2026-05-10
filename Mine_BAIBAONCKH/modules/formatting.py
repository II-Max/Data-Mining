"""Formatting module: export validated data to Excel and apply presentation formatting.

Provides DataFormatter class with `format` and `export_to_excel` methods.

Features:
- Executive summary with quality metrics
- Insights and top papers
- Formatted Excel export with multiple sheets
- Error handling and logging
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class DataFormatter:
    """Format and export mining results to Excel."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize formatter with configuration.
        
        Args:
            config: Config dict with OUTPUT_DIR
            
        Raises:
            OSError: If output directory cannot be created
        """
        self.config = config
        self.output_dir = Path(config.get("OUTPUT_DIR", "Data"))
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output directory ready: {self.output_dir}")
        except OSError as e:
            logger.error(f"Cannot create output directory {self.output_dir}: {e}")
            raise

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format dataframe for export.
        
        Currently a pass-through; can be extended for custom formatting.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Formatted copy of DataFrame
        """
        if df is None or df.empty:
            logger.warning("format() called with empty DataFrame")
            return pd.DataFrame()
        return df.copy()

    def _build_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Build executive summary with quality metrics.
        
        Args:
            df: Clean DataFrame
            
        Returns:
            Summary DataFrame with metrics
        """
        try:
            total = len(df)
            current_year = datetime.now().year

            # Calculate citation metrics
            if 'total_citations' in df.columns:
                citations_series = pd.to_numeric(df['total_citations'], errors='coerce').fillna(0)
                avg_citation = citations_series.mean()
                total_citation = citations_series.sum()
            else:
                avg_citation = 0
                total_citation = 0

            # Calculate hotness metrics
            if 'hotness_v' in df.columns:
                hotness_series = pd.to_numeric(df['hotness_v'], errors='coerce').fillna(0)
                avg_hotness = hotness_series.mean()
                max_hotness = hotness_series.max()
            else:
                avg_hotness = 0
                max_hotness = 0

            # Calculate Q-rank distribution
            if 'q_rank' in df.columns:
                q1 = len(df[df['q_rank'] == 'Q1'])
                q2 = len(df[df['q_rank'] == 'Q2'])
                q3 = len(df[df['q_rank'] == 'Q3'])
                q4 = len(df[df['q_rank'] == 'Q4'])
            else:
                q1 = q2 = q3 = q4 = 0

            high_tier_ratio = round(((q1 + q2) / total) * 100, 2) if total else 0

            # Calculate recency
            if 'year' in df.columns:
                years = pd.to_numeric(df['year'], errors='coerce')
                recent = len(df[years >= current_year - 2])
                recent_ratio = round((recent / total) * 100, 2) if total else 0
            else:
                recent_ratio = 0

            # Calculate DOI coverage
            if 'doi' in df.columns:
                doi_valid = df['doi'].astype(str).str.upper().ne('N/A').sum()
                doi_ratio = round((doi_valid / total) * 100, 2) if total else 0
            else:
                doi_ratio = 0

            # Calculate quality score (0-100)
            quality_score = round(
                min(
                    100,
                    (high_tier_ratio * 0.35) +
                    (recent_ratio * 0.25) +
                    (doi_ratio * 0.20) +
                    (min(avg_hotness, 20) * 1.0) +
                    10
                ),
                2
            )

            # Generate recommendation
            if quality_score >= 85:
                recommendation = "🟢 High-value dataset. Suitable for analytics & reporting."
            elif quality_score >= 70:
                recommendation = "🟡 Good dataset. Minor review recommended."
            else:
                recommendation = "🔴 Moderate quality. Further cleaning advised."

            summary = pd.DataFrame({
                "Metric": [
                    "Total Papers",
                    "Total Citations",
                    "Average Citations",
                    "Average Hotness",
                    "Peak Hotness",
                    "Q1 Papers",
                    "Q2 Papers",
                    "Q3 Papers",
                    "Q4 Papers",
                    "High Tier Ratio (Q1+Q2)",
                    "Recent Papers Ratio (2Y)",
                    "DOI Coverage",
                    "Executive Quality Score",
                    "Recommendation"
                ],
                "Value": [
                    total,
                    int(total_citation),
                    round(avg_citation, 2),
                    round(avg_hotness, 2),
                    round(max_hotness, 2),
                    q1,
                    q2,
                    q3,
                    q4,
                    f"{high_tier_ratio}%",
                    f"{recent_ratio}%",
                    f"{doi_ratio}%",
                    quality_score,
                    recommendation
                ]
            })

            logger.debug(f"Summary built: quality_score={quality_score}")
            return summary

        except Exception as e:
            logger.error(f"Error building summary: {e}", exc_info=True)
            raise

    def _build_insights(self, df: pd.DataFrame) -> pd.DataFrame:
        """Build insights from data (top sources, hot papers, etc).
        
        Args:
            df: Clean DataFrame
            
        Returns:
            Insights DataFrame
        """
        try:
            rows = []

            # Top journals/sources
            if 'journal' in df.columns:
                top_sources = df['journal'].fillna('N/A').value_counts().head(10)
                for source, count in top_sources.items():
                    rows.append({
                        'Insight Type': 'Top Source',
                        'Name': str(source)[:60],
                        'Value': count
                    })

            # Hottest papers
            if 'title' in df.columns and 'hotness_v' in df.columns:
                try:
                    top_hot = df.nlargest(5, 'hotness_v')
                    for _, row in top_hot.iterrows():
                        rows.append({
                            'Insight Type': 'Top Hot Paper',
                            'Name': str(row.get('title', 'N/A'))[:60],
                            'Value': row.get('hotness_v', 0)
                        })
                except Exception as e:
                    logger.debug(f"Error building hot papers: {e}")

            # Most cited papers
            if 'title' in df.columns and 'total_citations' in df.columns:
                try:
                    top_cited = df.nlargest(5, 'total_citations')
                    for _, row in top_cited.iterrows():
                        rows.append({
                            'Insight Type': 'Most Cited',
                            'Name': str(row.get('title', 'N/A'))[:60],
                            'Value': int(row.get('total_citations', 0))
                        })
                except Exception as e:
                    logger.debug(f"Error building cited papers: {e}")

            logger.debug(f"Insights built: {len(rows)} insights")
            return pd.DataFrame(rows) if rows else pd.DataFrame()

        except Exception as e:
            logger.error(f"Error building insights: {e}", exc_info=True)
            return pd.DataFrame()

    def export_to_excel(self, df: pd.DataFrame, filename: Optional[str] = None) -> Path:
        """Export formatted data to Excel with multiple sheets.
        
        Args:
            df: Data to export
            filename: Optional custom filename
            
        Returns:
            Path to exported file
            
        Raises:
            ValueError: If DataFrame empty
            IOError: If export fails
        """
        if df is None or df.empty:
            logger.error("Cannot export empty DataFrame")
            raise ValueError('No data to export')

        try:
            summary = self._build_summary(df)
            insights = self._build_insights(df)

            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            fname = filename or f"Executive_Report_{ts}.xlsx"
            out_path = self.output_dir / fname

            logger.info(f"Exporting to {out_path}")

            with pd.ExcelWriter(out_path, engine='xlsxwriter') as writer:
                # Sheet 1: Executive Summary
                summary.to_excel(writer, sheet_name='Executive Summary', index=False)
                ws_sum = writer.sheets['Executive Summary']
                ws_sum.set_column('A:A', 35)
                ws_sum.set_column('B:B', 60)

                # Sheet 2: Insights
                if not insights.empty:
                    insights.to_excel(writer, sheet_name='Insights', index=False)
                    ws_ins = writer.sheets['Insights']
                    ws_ins.set_column('A:A', 20)
                    ws_ins.set_column('B:B', 80)
                    ws_ins.set_column('C:C', 18)

                # Sheet 3: Clean Data
                df.to_excel(writer, sheet_name='Clean Data', index=False)
                ws = writer.sheets['Clean Data']
                ws.freeze_panes(1, 0)
                
                # Add autofilter
                try:
                    ws.autofilter(0, 0, len(df), len(df.columns) - 1)
                except Exception as e:
                    logger.debug(f"Could not add autofilter: {e}")

                # Auto-fit columns
                for col_num, value in enumerate(df.columns):
                    try:
                        col_str = str(value)
                        max_len = max(len(col_str), 
                                     df[value].astype(str).map(len).max() if len(df[value]) > 0 else 0) + 2
                        ws.set_column(col_num, col_num, min(max_len, 50))
                    except Exception as e:
                        logger.debug(f"Could not set column width for {value}: {e}")
                        ws.set_column(col_num, col_num, 20)

            logger.info(f"✓ Export successful: {out_path} ({len(df)} records)")
            return out_path

        except IOError as e:
            logger.error(f"IO error during export: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error during export: {e}", exc_info=True)
            raise
