def prettify_date(date):
    """Prettify your date"""
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    splitted_date = str(date).split('-')
    return f'{months[int(splitted_date[1])-1]} {splitted_date[2]}, {splitted_date[0]}'
