from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from api.repository.db import SWAPS_TABLE, Offline


class TokenSwaps(Model):
    class Meta(Offline):
        table_name = SWAPS_TABLE

    id = UnicodeAttribute(hash_key=True, null=False)
    amount_in = NumberAttribute(null=False)
    amount_out = NumberAttribute(null=False)
    token_in = UnicodeAttribute(null=False)
    token_out = UnicodeAttribute(null=False)
    created_at = UTCDateTimeAttribute(null=False)
