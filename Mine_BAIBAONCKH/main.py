"""Main entrypoint for Research - Mining pipeline.

This script orchestrates Mining -> Validating -> Formatting steps. It supports
both interactive prompts and command line options (topic, year, mode, limit).
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path
from utils.config import load_config
from utils.logger import get_logger

logger = get_logger(__name__)

# lazy imports for modules
try:
    from modules.mining import MiningEngine
    from modules.validating import DataValidator
    from modules.formatting import DataFormatter
except Exception as e:
    logger.error("Required modules not found. Did you run this from project root? %s", e)
    raise


def validate_inputs(topic: str, year: int, mode: str, limit: int) -> None:
    """Validate user inputs before processing.
    
    Args:
        topic: Research topic to search
        year: Start year filter
        mode: Search mode (top_tier or all)
        limit: Max number of papers
        
    Raises:
        ValueError: If any input is invalid
    """
    current_year = datetime.now().year
    
    # Validate topic
    if not topic or len(topic.strip()) < 2:
        raise ValueError("Topic must be at least 2 characters long")
    if len(topic) > 500:
        raise ValueError("Topic too long (max 500 chars)")
    
    # Validate year
    if year < 1900:
        raise ValueError("Year must be >= 1900")
    if year > current_year:
        raise ValueError(f"Year cannot be in the future (current: {current_year})")
    
    # Validate mode
    if mode not in ('top_tier', 'all'):
        raise ValueError("Mode must be 'top_tier' or 'all'")
    
    # Validate limit
    if limit < 1:
        raise ValueError("Limit must be >= 1")
    if limit > 1000:
        raise ValueError("Limit must be <= 1000 (SerpApi rate limit)")


def parse_args():
    p = argparse.ArgumentParser(
        description='Research Mining Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "deep learning" --year 2020
  python main.py -t "quantum computing" -y 2018 -m all --limit 100
  python main.py --no_prompt  (interactive mode)
        """
    )
    p.add_argument('--topic', '-t', help='Research topic to search for')
    p.add_argument('--year', '-y', type=int, help='Filter from year (YYYY)', default=2020)
    p.add_argument('--mode', '-m', choices=['top_tier', 'all'], default='top_tier',
                   help='Search mode: top_tier (Nature, Science, IEEE, etc.) or all sources')
    p.add_argument('--limit', '-n', type=int, default=40,
                   help='Maximum number of papers to fetch (1-1000)')
    p.add_argument('--no_prompt', action='store_true', help='Do not prompt interactively (use defaults)')
    return p.parse_args()


class Pipeline:
    def __init__(self, config):
        self.config = config
        self.miner = MiningEngine(config)
        self.validator = DataValidator(config)
        self.formatter = DataFormatter(config)

    def run(self, topic: str, year: int, mode: str, limit: int) -> None:
        """Run the complete mining pipeline.
        
        Args:
            topic: Research topic
            year: Start year
            mode: Search mode
            limit: Max papers to fetch
            
        Raises:
            Exception: If any pipeline step fails
        """
        try:
            logger.info('Starting pipeline: topic=%s year=%s mode=%s limit=%s', topic, year, mode, limit)

            df_raw = self.miner.extract(query=topic, year_start=year, limit=limit, mode=mode)
            if df_raw is None or df_raw.empty:
                logger.warning('No data mined from API')
                print("⚠️  No results found for this query. Try different keywords or relaxed filters.")
                return
                
            logger.info('✓ Mined %d records', len(df_raw))

            df_valid = self.validator.validate(df_raw)
            if df_valid is None or df_valid.empty:
                logger.warning('No valid records after validation')
                print("⚠️  No records passed validation. Check data quality.")
                return
                
            logger.info('✓ Validated %d records (removed %d duplicates/invalid)', 
                       len(df_valid), len(df_raw) - len(df_valid))

            df_formatted = self.formatter.format(df_valid)
            out_path = self.formatter.export_to_excel(df_formatted)
            logger.info('✓ Exported results to %s', out_path)
            print(f"\n✅ Pipeline complete. Output: {out_path}")
            
        except Exception as e:
            logger.error('Pipeline failed: %s', e, exc_info=True)
            print(f"\n❌ Error: {e}")
            raise


def main():
    try:
        args = parse_args()
        logger.info('Pipeline started with args: %s', args)
        
        # Load config (this validates API key is set)
        try:
            cfg = load_config()
        except ValueError as e:
            logger.error('Configuration error: %s', e)
            print(f"❌ {e}")
            sys.exit(1)

        # Get topic from args or interactive prompt
        topic = args.topic
        if not topic and not args.no_prompt:
            topic = input('📝 Enter research topic: ').strip()

        if not topic:
            logger.error('No topic provided. Exiting.')
            print("❌ Topic is required.")
            sys.exit(1)

        # Get year
        year = args.year
        if not args.no_prompt:
            try:
                y_in = input(f'📅 Filter from year (YYYY) [{year}]: ').strip()
                if y_in:
                    year = int(y_in)
            except ValueError:
                logger.warning('Invalid year input, using default: %s', year)
                pass

        # Get mode
        mode = args.mode
        if not args.no_prompt:
            m_in = input(f'🎯 Choose mode (top_tier/all) [{mode}]: ').strip()
            if m_in in ('top_tier', 'all'):
                mode = m_in

        # Get limit
        limit = args.limit
        if not args.no_prompt:
            try:
                n_in = input(f'📊 Limit number of papers [{limit}]: ').strip()
                if n_in:
                    limit = int(n_in)
            except ValueError:
                logger.warning('Invalid limit input, using default: %s', limit)
                pass

        # Validate all inputs
        try:
            validate_inputs(topic, year, mode, limit)
        except ValueError as e:
            logger.error('Input validation failed: %s', e)
            print(f"❌ {e}")
            sys.exit(1)

        # Run pipeline
        pipeline = Pipeline(cfg)
        pipeline.run(topic=topic, year=year, mode=mode, limit=limit)

    except KeyboardInterrupt:
        logger.info('Pipeline interrupted by user')
        print("\n⏹️  Pipeline cancelled.")
        sys.exit(0)
    except Exception as e:
        logger.error('Unexpected error: %s', e, exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
