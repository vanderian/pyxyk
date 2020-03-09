from pynamodb.attributes import UnicodeAttribute, NumberAttribute, VersionAttribute
from pynamodb.models import Model

from api.repository.db import POOLS_TABLE, Offline


class LiquidityPools(Model):
    class Meta(Offline):
        table_name = POOLS_TABLE

    token_symbol = UnicodeAttribute(hash_key=True, null=False)
    pool_native = NumberAttribute(null=False)
    pool_token = NumberAttribute(null=False)
    version = VersionAttribute()

    def as_dict(self):
        return {'token_symbol': self.token_symbol, 'pool_native': self.pool_native, 'pool_token': self.pool_token}
