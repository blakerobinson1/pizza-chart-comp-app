#!/usr/bin/env python3
"""
Test script to verify the new structure works correctly
"""
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from config import AVAILABLE_SEASONS, MODEL_CONFIG
        logger.info("✅ Config module imported successfully")
        
        from data.data_manager import data_manager
        logger.info("✅ Data manager imported successfully")
        
        from models.base_model import BaseModel
        logger.info("✅ Base model imported successfully")
        
        from models.qb.qb_model import QBExpectedCompletionModel
        logger.info("✅ QB model imported successfully")
        
        from analytics.player_stats import player_stats_calculator
        logger.info("✅ Player stats calculator imported successfully")
        
        from visualization.pizza_chart import pizza_chart_visualizer
        logger.info("✅ Pizza chart visualizer imported successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_data_loading():
    """Test data loading functionality"""
    try:
        from data.data_manager import data_manager
        
        # Check if data files exist
        data_files = list(Path("data/pbp").glob("pbp_*.parquet"))
        if data_files:
            logger.info(f"✅ Found {len(data_files)} data files")
            
            # Try to load one file
            test_df = data_manager.load_pbp_by_season(2024)
            if not test_df.empty:
                logger.info(f"✅ Successfully loaded {len(test_df)} plays from 2024")
                return True
            else:
                logger.warning("⚠️ Loaded dataframe is empty")
                return False
        else:
            logger.warning("⚠️ No data files found in data/pbp/")
            return False
            
    except Exception as e:
        logger.error(f"❌ Data loading error: {e}")
        return False

def test_configuration():
    """Test configuration settings"""
    try:
        from config import AVAILABLE_SEASONS, MODEL_CONFIG
        
        logger.info(f"✅ Available seasons: {AVAILABLE_SEASONS}")
        logger.info(f"✅ Model config keys: {list(MODEL_CONFIG.keys())}")
        
        # Check if directories exist
        from config import DATA_DIR, MODELS_DIR, CACHE_DIR
        for directory in [DATA_DIR, MODELS_DIR, CACHE_DIR]:
            if directory.exists():
                logger.info(f"✅ Directory exists: {directory}")
            else:
                logger.warning(f"⚠️ Directory missing: {directory}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting structure tests...")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_configuration),
        ("Data Loading Tests", test_data_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            logger.info(f"✅ {test_name} passed")
        else:
            logger.error(f"❌ {test_name} failed")
    
    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! The new structure is working correctly.")
        logger.info("You can now run: python scripts/train_models.py")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 