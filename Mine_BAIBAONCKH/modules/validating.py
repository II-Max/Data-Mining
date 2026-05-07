"""Validation module: encapsulates data cleaning and validation logic.

Provides DataValidator class with a `validate` method that accepts a
pandas.DataFrame (raw mined data) and returns a validated/normalized DataFrame.

Features:
- Comprehensive data type normalization
- Duplicate removal
- Citation threshold filtering
- DOI validation
- Null handling
"""
from typing import Dict, Any, Optional
import logging
import pandas as pd
import re

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate and normalize mining results."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize validator with configuration.
        
        Args:
            config: Config dict with MIN_CITATIONS setting
        """
        self.config = config
        self.min_citations = int(config.get("MIN_CITATIONS", 0))
        logger.info(f"DataValidator initialized with min_citations={self.min_citations}")

    def _validate_doi(self, doi: Any) -> str:
        """Validate DOI format.
        
        Args:
            doi: DOI string or value
            
        Returns:
            Valid DOI string or 'N/A'
        """
        if pd.isna(doi) or str(doi).upper() in ("NA", "N/A", "", "NONE"):
            return "N/A"
        
        doi_str = str(doi).strip()
        if re.search(r"10\.\d{4,9}/", doi_str):
            return doi_str
        return "N/A"

    def _validate_year(self, year: Any) -> int:
        """Validate and convert year to int.
        
        Args:
            year: Year value
            
        Returns:
            Valid year as int or 0 if invalid
        """
        try:
            if pd.isna(year):
                return 0
            year_int = int(year)
            if 1900 <= year_int <= 2100:
                return year_int
            return 0
        except (ValueError, TypeError):
            return 0

    def _validate_citations(self, citations: Any) -> int:
        """Validate and convert citations count.
        
        Args:
            citations: Citation count
            
        Returns:
            Valid citation count or 0
        """
        try:
            if pd.isna(citations):
                return 0
            citations_int = int(float(citations))
            return max(0, citations_int)
        except (ValueError, TypeError):
            return 0

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and normalize dataframe produced by mining module.
        
        Args:
            df: Raw DataFrame from mining
            
        Returns:
            Cleaned and validated DataFrame
            
        Raises:
            TypeError: If input is not a DataFrame
        """
        if not isinstance(df, pd.DataFrame):
            logger.error(f"Expected DataFrame, got {type(df)}")
            raise TypeError("Input must be a pandas DataFrame")
        
        if df is None or df.empty:
            logger.warning("Input DataFrame is empty, returning empty DataFrame")
            return pd.DataFrame()

        original_count = len(df)
        logger.info(f"Validating {original_count} records")

        try:
            # Normalize string columns - strip whitespace
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].astype(str).str.strip()

            # Normalize case
            if "title" in df.columns:
                df['title'] = df['title'].str.upper()

            if 'journal' in df.columns:
                df['journal'] = df['journal'].str.title()

            if 'authors' in df.columns:
                df['authors'] = df['authors'].str.title()

            # Validate DOI format
            if 'doi' in df.columns:
                df['doi'] = df['doi'].apply(self._validate_doi)

            # Validate and convert year
            if 'year' in df.columns:
                df['year'] = df['year'].apply(self._validate_year)

            # Validate and convert citations
            if 'total_citations' in df.columns:
                df['total_citations'] = df['total_citations'].apply(self._validate_citations)

            # Validate velocity/hotness
            if 'hotness_v' in df.columns:
                df['hotness_v'] = pd.to_numeric(df['hotness_v'], errors='coerce').fillna(0)
                df['hotness_v'] = df['hotness_v'].apply(lambda x: max(0, x))

            # Fill remaining NaNs
            df = df.fillna('N/A')

            # Remove duplicates by title (keeping first occurrence)
            if 'title' in df.columns:
                before_dedup = len(df)
                df = df.drop_duplicates(subset=['title'], keep='first')
                duplicates_removed = before_dedup - len(df)
                if duplicates_removed > 0:
                    logger.info(f"Removed {duplicates_removed} duplicate records")

            # Apply citation threshold
            if 'total_citations' in df.columns and self.min_citations > 0:
                before_filter = len(df)
                df = df[df['total_citations'] >= self.min_citations]
                filtered = before_filter - len(df)
                if filtered > 0:
                    logger.info(f"Filtered out {filtered} records below citation threshold ({self.min_citations})")

            # Reset index
            df = df.reset_index(drop=True)

            final_count = len(df)
            removed_count = original_count - final_count
            logger.info(f"Validation complete: {final_count} valid records (removed {removed_count})")

            return df

        except Exception as e:
            logger.error(f"Validation error: {e}", exc_info=True)
            raise
