# Pizza Chart Comparison App

A machine learning application for generating predictive football statistics and visualizing them in pizza charts for player comparison.

## 🎯 Objective

This application uses machine learning models to generate effective predictive statistics for football players and visualizes them in "pizza" charts for easy comparison. The system is designed for efficiency - models are trained once and used to create datasets by position, which are then used to generate charts without retraining models for each new player or chart generation.

## 🏗️ Architecture

### New Structure

```
pizza-chart-comp-app/
├── src/
│   ├── config.py                 # Centralized configuration
│   ├── app.py                    # Main Dash application
│   ├── data/
│   │   └── data_manager.py       # Centralized data management
│   ├── models/
│   │   ├── base_model.py         # Base model class
│   │   └── qb/
│   │       └── qb_model.py       # QB-specific model
│   ├── analytics/
│   │   └── player_stats.py       # Player statistics calculator
│   └── visualization/
│       └── pizza_chart.py        # Pizza chart visualizations
├── scripts/
│   └── train_models.py           # Script to train models and generate datasets
├── data/
│   ├── pbp/                      # Play-by-play data
│   └── datasets/                 # Generated player statistics
├── models/
│   └── trained/                  # Trained model files
└── cache/                        # Model cache
```

### Key Improvements

1. **Modular Design**: Clear separation of concerns with dedicated modules for data, models, analytics, and visualization
2. **Centralized Configuration**: All settings and paths in one place
3. **Efficient Model Usage**: Models are trained once and reused for dataset generation
4. **Dataset Generation**: Pre-computed player statistics for fast chart generation
5. **Clean Architecture**: Base classes and inheritance for consistent model implementation

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate pizza-chart-comp-app
```

### 2. Data Preparation

Ensure you have play-by-play data files in `data/pbp/`:
- `pbp_2018.parquet`
- `pbp_2019.parquet`
- `pbp_2020.parquet`
- `pbp_2021.parquet`
- `pbp_2022.parquet`
- `pbp_2023.parquet`
- `pbp_2024.parquet`

### 3. Train Models and Generate Datasets

```bash
# Run the setup script to train models and generate datasets
python scripts/train_models.py
```

This will:
- Train the QB expected completion model
- Generate QB and RB player statistics datasets
- Save everything to the appropriate directories

### 4. Run the Application

```bash
# Start the Dash application
python -m src.app
```

The app will be available at `http://localhost:8050`

## 📊 Features

### Supported Positions

- **QB (Quarterback)**: Completion percentage over expected, EPA per play, air yards, interceptions, sacks, rushing, turnovers, touchdowns
- **RB (Running Back)**: Yards per attempt, EPA per play, first down rate, touchdown rate, breakaway runs
- **WR (Wide Receiver)**: Coming soon
- **TE (Tight End)**: Coming soon

### Visualization Types

1. **Pizza Charts**: Side-by-side comparison of player statistics
2. **Radar Charts**: Multi-dimensional player comparison

### Model Types

- **Expected Completion Model**: Predicts completion probability based on play context
- **Future Models**: Will include rushing, receiving, and other position-specific models

## 🔧 Usage

### Web Interface

1. Select a position (QB, RB, WR, TE)
2. Choose a season (2018-2024)
3. Select up to 4 players to compare
4. Click "Train Models" to train new models (if needed)
5. Click "Generate Charts" to create visualizations

### Programmatic Usage

```python
from src.analytics.player_stats import player_stats_calculator
from src.visualization.pizza_chart import pizza_chart_visualizer

# Generate QB statistics
qb_stats = player_stats_calculator.generate_qb_dataset(
    players=['Patrick Mahomes', 'Josh Allen'], 
    seasons=[2023]
)

# Create pizza chart
fig = pizza_chart_visualizer.create_qb_pizza_chart(
    qb_stats, 
    players=['Patrick Mahomes', 'Josh Allen'], 
    season=2023
)
```

## 🏗️ Development

### Adding New Positions

1. Create a new model class inheriting from `BaseModel`
2. Implement the `preprocess_data` method
3. Add position configuration to `config.py`
4. Create position-specific statistics calculator
5. Add visualization methods

### Adding New Metrics

1. Update the position configuration in `config.py`
2. Add calculation logic in the appropriate statistics calculator
3. Update visualization methods to include the new metric

## 📁 Directory Structure

- **`src/`**: Main application code
- **`data/`**: Raw data and generated datasets
- **`models/`**: Trained model files
- **`scripts/`**: Utility scripts for training and setup
- **`cache/`**: Model cache and temporary files

## 🔄 Data Flow

1. **Raw Data**: Play-by-play data loaded from `data/pbp/`
2. **Model Training**: Models trained on historical data and saved to `models/trained/`
3. **Dataset Generation**: Player statistics calculated and saved to `data/datasets/`
4. **Visualization**: Charts generated from pre-computed datasets for fast performance

## 🎯 Efficiency Benefits

- **No Model Retraining**: Models trained once and reused
- **Fast Chart Generation**: Pre-computed datasets enable instant visualization
- **Scalable Architecture**: Easy to add new positions and metrics
- **Cached Results**: Datasets saved for quick access

## 🐛 Troubleshooting

### Common Issues

1. **Missing Data**: Ensure play-by-play files exist in `data/pbp/`
2. **Import Errors**: Make sure you're in the correct conda environment
3. **Model Training Failures**: Check that data files are not corrupted
4. **Chart Generation Issues**: Verify that datasets have been generated

### Logs

The application uses Python logging. Check console output for detailed error messages and progress information.

## 🤝 Contributing

1. Follow the modular architecture
2. Add tests for new functionality
3. Update documentation for new features
4. Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.







By Me:
1. Models exist at src/models/position level
2. scripts/train_models.py trains and scores them
2a. This script creates new datasets containing all relevant data for use in pizza chart creation
3. visualization/pizza_chart.py reads these datasets and builds the pizza charts from them
4. app.py generates the app and calls the pizza chart creation


Goal Metrics (QB):
1. Completion Percentage over Expected (CPOE) ***
2. EPA per Play
3. Air Yards over Expected (AYOE) ***
4. Interceptions per Attempt
5. Sacks over Expected (SOE) ***
6. Rushing Yards over Expected (RYOE) ***
7. Turnover worthy Play rate ***
8. Touchdowns over Expected (TDOE) ***

To-Do:
- work to be done in train_models.py
- Continued troubleshooting
1. Read in PBP datasets, from API? (probably don't need them stored locally) 
3. Train, save, and score xcomp cpoe
4. Generate pizza chart dataset containing xcomp cpoe
5. Print the dataset to the app






