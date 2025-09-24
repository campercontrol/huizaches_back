def format_numbers_commas_currency(number, symbol, acronym):
    """Format a number with commas as thousand separators."""
    return symbol + "{:,.2f}".format(number) + " " + acronym