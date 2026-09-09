"""Tests for the data cleaning module."""

import pandas as pd
import pytest

from ecommerce_analysis.data_cleaning import (
    remove_duplicates,
    handle_missing_values,
    remove_invalid_transactions,
    add_features,
    clean_data,
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "InvoiceNo": ["INV001", "INV001", "INV002", "INV003", "INV004", "INV005"],
            "StockCode": ["A", "A", "B", "C", "D", "E"],
            "Description": [
                "Product A",
                "Product A",
                "Product B",
                "Product C",
                None,
                "Product E",
            ],
            "Quantity": [5, 5, -2, 3, 0, 10],
            "InvoiceDate": pd.to_datetime(
                [
                    "2023-01-01",
                    "2023-01-01",
                    "2023-01-02",
                    "2023-01-03",
                    "2023-01-04",
                    "2023-01-05",
                ]
            ),
            "UnitPrice": [10.0, 10.0, 15.0, -5.0, 20.0, 25.0],
            "CustomerID": [1.0, 1.0, 2.0, None, 4.0, 5.0],
            "Country": ["UK", "UK", "France", "Germany", "UK", "UK"],
        }
    )


def test_remove_duplicates(sample_df):
    """Test that duplicate rows are removed."""
    result = remove_duplicates(sample_df)

    # Should have 5 rows instead of 6 (one duplicate removed)
    assert len(result) == 5
    # Should not contain duplicate InvoiceNo
    assert result["InvoiceNo"].duplicated().sum() == 0


def test_handle_missing_values_drops_customer_id(sample_df):
    """Test that rows with missing CustomerID are dropped."""
    result = handle_missing_values(sample_df)

    # Row with CustomerID=None should be removed
    assert result["CustomerID"].isna().sum() == 0
    assert len(result) == 5  # 6 rows - 1 with missing CustomerID


def test_handle_missing_values_fills_description(sample_df):
    """Test that missing Description is filled with 'Unknown'."""
    result = handle_missing_values(sample_df)

    # Description should not have missing values
    assert result["Description"].isna().sum() == 0
    # The missing Description should be 'Unknown'
    unknown_count = (result["Description"] == "Unknown").sum()
    assert unknown_count == 1


def test_remove_invalid_transactions_removes_negative_prices(sample_df):
    """Test that negative prices are removed."""
    result = remove_invalid_transactions(sample_df)

    # No negative UnitPrice should remain
    assert (result["UnitPrice"] < 0).sum() == 0


def test_remove_invalid_transactions_keeps_negative_quantities(sample_df):
    """Test that negative quantities (returns) are kept."""
    result = remove_invalid_transactions(sample_df)

    # Negative quantities should still exist (returns are valid)
    assert (result["Quantity"] < 0).sum() > 0


def test_remove_invalid_transactions_removes_zero_quantity(sample_df):
    """Test that zero quantities are removed."""
    result = remove_invalid_transactions(sample_df)

    # No zero Quantity should remain
    assert (result["Quantity"] == 0).sum() == 0


def test_add_features_calculates_total_price(sample_df):
    """Test that TotalPrice is calculated correctly."""
    result = add_features(sample_df)

    # Check TotalPrice column exists
    assert "TotalPrice" in result.columns
    # Check first row: 5 * 10.0 = 50.0
    assert result.iloc[0]["TotalPrice"] == 50.0
    # Check third row: -2 * 15.0 = -30.0
    assert result.iloc[2]["TotalPrice"] == -30.0


def test_add_features_creates_year_month(sample_df):
    """Test that YearMonth column is created."""
    result = add_features(sample_df)

    # Check YearMonth column exists
    assert "YearMonth" in result.columns
    # Check that YearMonth has correct values
    assert str(result.iloc[0]["YearMonth"]) == "2023-01"


def test_clean_data_pipeline(sample_df):
    """Test that the complete pipeline runs end-to-end."""
    result = clean_data(sample_df)

    # Check that result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    # Check that all cleaning steps were applied
    assert result["CustomerID"].isna().sum() == 0  # Missing values handled
    assert result["UnitPrice"].min() > 0  # No negative prices
    assert "TotalPrice" in result.columns  # Features added
    assert "YearMonth" in result.columns  # Features added


def test_clean_data_handles_empty_dataframe():
    """Test that clean_data handles empty DataFrame gracefully."""
    empty_df = pd.DataFrame(
        {
            "InvoiceNo": [],
            "StockCode": [],
            "Description": [],
            "Quantity": [],
            "InvoiceDate": pd.to_datetime([]),
            "UnitPrice": [],
            "CustomerID": [],
            "Country": [],
        }
    )

    result = clean_data(empty_df)

    # Should return empty DataFrame without errors
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
