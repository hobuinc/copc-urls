"""
model for lmabda
"""
import pytz

from pynamodb.attributes import (
    UnicodeAttribute, UTCDateTimeAttribute, BooleanAttribute
)
from pynamodb.models import Model

from constants import ENV, AWS_REGION

def get_now():
    import datetime
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

def create_table_name(table_name):
    """
    create table to name for dynamodb
    """
    return f'{ENV}-{table_name}'


class ShortURL(Model):
    """
    A DynamoDB VideoWatch
    """

    class Meta:
        """
        set meta of table
        """
        table_name = create_table_name("copc-urls-data-store")
        region = AWS_REGION

    url = UnicodeAttribute(hash_key=True, null=False)
    state = UnicodeAttribute(null=False) # render state as a blob of json
    created_at = UTCDateTimeAttribute(default=get_now())


# automatically creates a table in dynamo db if doesnt exist.
if not ShortURL.exists():
    ShortURL.create_table(wait=True, billing_mode="PAY_PER_REQUEST")
