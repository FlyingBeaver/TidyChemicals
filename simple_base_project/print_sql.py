from sql_formatter.core import format_sql
#from prettytable import PrettyTable


def print_sql(queryset):
    if str(type(queryset)) != "<class 'django.db.models.query.QuerySet'>":
        raise TypeError("The argument must be django QuerySet")
    print(format_sql(str(queryset.query)))
