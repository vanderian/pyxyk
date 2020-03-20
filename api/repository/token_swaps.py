from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model

from api.repository.db import SWAPS_TABLE, Offline
from api.schema.token_swap_schema import TokenSwapSchema


class TokenSwaps(Model):
    class Meta(Offline):
        table_name = SWAPS_TABLE

    id = UnicodeAttribute(hash_key=True, null=False)
    amount_in = NumberAttribute(null=False)
    amount_out = NumberAttribute(null=False)
    token_in = UnicodeAttribute(null=False)
    token_out = UnicodeAttribute(null=False)
    created_at = UTCDateTimeAttribute(null=False)

    @staticmethod
    def find_all(req_page_size: int, req_next_id: int, condition: Condition):
        schema = TokenSwapSchema()
        items = []
        while True:
            # very inefficient, scan goes through all records; we should feed the data to eg. elastic
            result = TokenSwaps.scan(condition, limit=req_page_size, last_evaluated_key=req_next_id)
            items += list(map(lambda ts: schema.dump(ts), result))
            req_next_id = result.last_evaluated_key
            if len(items) == req_page_size or req_next_id is None:
                break

        next_id = None
        if result.last_evaluated_key is not None:
            # ref: repository.token_swaps.TokenSwaps.id: UnicodeAttribute('S')
            next_id = result.last_evaluated_key['id']['S']
        return items, next_id
