"""Mining module: encapsulates data extraction logic from Google Scholar via SerpApi.

Provides a MiningEngine class with a single public method `extract` that
returns a pandas.DataFrame of mined records.

Features:
- Retry logic with exponential backoff
- Rate limiting control
- Comprehensive error handling
- Timeout support
"""
from typing import List, Dict, Any, Optional
import os
import time
import re
from datetime import datetime
import logging
import pandas as pd

try:
    from serpapi import GoogleSearch
except ImportError:
    try:
        # Try alternative import if google-search-results is used
        from google_search_results import GoogleSearch
    except ImportError:
        GoogleSearch = None

logger = logging.getLogger(__name__)


class MiningEngine:
    """Extract academic papers from Google Scholar via SerpApi."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize MiningEngine with configuration.
        
        Args:
            config: Configuration dict with SERPAPI_KEY and optional rate limit settings
            
        Raises:
            ValueError: If SERPAPI_KEY is not configured
        """
        self.config = config
        self.api_key = config.get("SERPAPI_KEY") or os.getenv("SERPAPI_KEY")
        self.output_dir = config.get("OUTPUT_DIR", "Data")
        self.rate_limit = float(config.get("API_RATE_LIMIT", 1.0))
        self.max_retries = int(config.get("MAX_RETRIES", 3))
        self.timeout = int(config.get("REQUEST_TIMEOUT", 30))
        
        if not self.api_key:
            raise ValueError("SERPAPI_KEY not configured")

    def _parse_metadata(self, item: Dict[str, Any]) -> tuple:
        """Parse paper metadata from SerpApi response.
        
        Args:
            item: Single result item from SerpApi
            
        Returns:
            Tuple of (authors, journal, year, access_status, doi)
        """
        summary = item.get("publication_info", {}).get("summary", "NA")
        authors, journal, year = "NA", "NA", "NA"

        if summary != "NA":
            try:
                parts = summary.split(" - ")
                if len(parts) >= 1:
                    authors = parts[0].strip()
                if len(parts) >= 2:
                    source_part = parts[1]
                    year_match = re.search(r'\b(19|20)\d{2}\b', source_part)
                    if year_match:
                        year = int(year_match.group())
                        journal = source_part.split(str(year))[0].strip().rstrip(',')
                    else:
                        journal = source_part.strip()
            except Exception as e:
                logger.debug(f"Error parsing metadata: {e}")

        # Extract DOI
        doi_pattern = r"10\.\d{4,9}/[-._;()/:\w]+"
        try:
            doi_match = re.search(doi_pattern, item.get("link", ""), re.IGNORECASE)
            doi = doi_match.group(0) if doi_match else "N/A"
        except Exception:
            doi = "N/A"

        # Determine access status
        resources = item.get("resources", [])
        access = "Open Access (PDF)" if resources and "pdf" in str(resources).lower() else "Locked/Paywall"

        return authors, journal, year, access, doi

    def _calculate_velocity(self, citations: int, year: int) -> float:
        """Calculate citation velocity (citations per year).
        
        Args:
            citations: Total citation count
            year: Publication year
            
        Returns:
            Citation velocity rounded to 2 decimals
        """
        current_year = datetime.now().year
        try:
            if isinstance(year, str):
                year = int(year)
            years_published = max(1, current_year - year + 1)
            return round(citations / years_published, 2)
        except (ValueError, TypeError):
            return 0.0

    def _assign_q_rank(self, velocity: float) -> str:
        """Assign quartile rank based on citation velocity.
        
        Args:
            velocity: Citation velocity
            
        Returns:
            Q-rank string: Q1, Q2, Q3, or Q4
        """
        if velocity >= 15.0:
            return "Q1"
        if velocity >= 5.0:
            return "Q2"
        if velocity >= 1.0:
            return "Q3"
        return "Q4"

    def _call_api_with_retry(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call SerpApi with retry logic and exponential backoff.
        
        Args:
            params: SerpApi request parameters
            
        Returns:
            API response dict or None if all retries failed
            
        Raises:
            RuntimeError: If serpapi package not available
        """
        if GoogleSearch is None:
            raise RuntimeError("serpapi package not available. Install: pip install serpapi")

        for attempt in range(self.max_retries):
            try:
                logger.debug(f"API call attempt {attempt + 1}/{self.max_retries}")
                search = GoogleSearch(params)
                results = search.get_dict()
                
                if "error" not in results:
                    logger.debug("API call successful")
                    return results
                else:
                    error_msg = results.get("error", "Unknown error")
                    logger.warning(f"API error: {error_msg}")
                    
            except Exception as e:
                logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
            
            # Exponential backoff: 1s, 2s, 4s
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        logger.error(f"Failed after {self.max_retries} retries")
        return None

    def extract(self, query: str, year_start: int = 2020, limit: int = 40, 
                mode: str = "top_tier") -> pd.DataFrame:
        """Extract papers from Google Scholar via SerpApi.
        
        Args:
            query: Search query string
            year_start: Start year filter
            limit: Maximum papers to fetch (max 1000)
            mode: 'top_tier' (Nature, Science, IEEE, ACM, Cell) or 'all'
            
        Returns:
            DataFrame with normalized columns: title, doi, q_rank, access_status,
                     year, authors, journal, total_citations, hotness_v, snippet, link
                     
        Raises:
            ValueError: If parameters invalid
            RuntimeError: If API not available
        """
        if not self.api_key:
            raise RuntimeError("SerpApi key not configured (SERPAPI_KEY).")

        if GoogleSearch is None:
            raise RuntimeError("serpapi package not available in the environment.")

        if limit < 1 or limit > 1000:
            raise ValueError("Limit must be between 1 and 1000")
        if year_start < 1900 or year_start > datetime.now().year:
            raise ValueError(f"Year must be between 1900 and {datetime.now().year}")

        # Build search filter based on mode
        q_filter = ""
        if mode == "top_tier":
            q_filter = ' source:"Nature" OR source:"Science" OR source:"IEEE" OR source:"ACM" OR source:"Cell"'
        elif mode == "all":
            q_filter = ""
        else:
            raise ValueError("Mode must be 'top_tier' or 'all'")

        records: List[Dict[str, Any]] = []
        logger.info(f"Starting mining: query='{query}', year_start={year_start}, mode={mode}, limit={limit}")

        for start_idx in range(0, limit, 20):
            try:
                num_to_fetch = min(20, limit - start_idx)
                params = {
                    "engine": "google_scholar",
                    "q": f"{query}{q_filter} after:{year_start}",
                    "api_key": self.api_key,
                    "start": start_idx,
                    "num": num_to_fetch
                }

                results = self._call_api_with_retry(params)
                if results is None:
                    logger.warning(f"API returned None at start_idx={start_idx}, stopping mining")
                    break

                if "error" in results:
                    logger.warning(f"API error: {results.get('error')}, stopping")
                    break

                organic = results.get("organic_results", [])
                if not organic:
                    logger.info(f"No results at start_idx={start_idx}, stopping")
                    break

                logger.debug(f"Fetched {len(organic)} results at start_idx={start_idx}")

                for item in organic:
                    try:
                        authors, journal, year, access, doi = self._parse_metadata(item)

                        # Skip if year invalid or before filter
                        if year == "NA":
                            continue
                        
                        year_int = int(year) if isinstance(year, (int, str)) else 0
                        if year_int < year_start:
                            continue

                        citations = item.get("inline_links", {}).get("cited_by", {}).get("total", 0)
                        velocity = self._calculate_velocity(citations, year)
                        q_rank = self._assign_q_rank(velocity)

                        records.append({
                            "title": item.get("title", "N/A").upper(),
                            "doi": doi,
                            "q_rank": q_rank,
                            "access_status": access,
                            "year": year_int,
                            "authors": authors,
                            "journal": journal if journal != "" else "N/A",
                            "total_citations": citations,
                            "hotness_v": velocity,
                            "snippet": item.get("snippet", "N/A").replace("\n", " "),
                            "link": item.get("link", "N/A")
                        })
                    except Exception as e:
                        logger.debug(f"Error processing item: {e}")
                        continue

                # Apply rate limiting
                if len(records) < limit:
                    time.sleep(self.rate_limit)

                if len(records) >= limit:
                    logger.info(f"Reached limit of {limit} records")
                    break

            except Exception as e:
                logger.error(f"Error in extraction loop at start_idx={start_idx}: {e}")
                continue

        logger.info(f"Mining complete: extracted {len(records)} records")
        
        if not records:
            logger.warning("No records extracted")
            return pd.DataFrame()
        
        df = pd.DataFrame(records)
        return df
