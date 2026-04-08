# Data Directory

## Structure

- **raw/** - Place your original dataset files here
- **processed/** - Preprocessed data will be saved here automatically

## Dataset Information

**Name:** [Dataset name]  
**Source:** [Dataset source/link]  
**Format:** CSV / Excel / Other  
**Size:** [Number of rows and columns]

## Instructions

1. Download your dataset
2. Place it in the `raw/` directory
3. Update the path in `config/config.yaml` or `src/data_preprocessing.py`
4. Run preprocessing: `python src/data_preprocessing.py`

## Notes

- Do not modify files in `processed/` directory manually
- Large data files are gitignored by default
- Add dataset citation/reference if required
