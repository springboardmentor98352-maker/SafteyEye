import pytest
from utils.data_loader import download_dataset, load_data

def test_download_dataset(mocker):
    mock_kaggle_api = mocker.patch('utils.data_loader.kaggle.api')
    download_dataset()
    mock_kaggle_api.dataset_download_files.assert_called_once_with(
        'snehilsanyal/construction-site-safety-image-dataset-roboflow',
        path='data/raw',
        unzip=True
    )

def test_load_data():
    data = load_data('data/processed')
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(item, dict) for item in data)  # Assuming each item is a dictionary