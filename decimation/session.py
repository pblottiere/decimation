from itertools import chain
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor

class Session(object):

    def __init__(self):
        self.PG_USER="blottiere"
        self.PG_PASSWORD=""
        self.PG_HOST="localhost"
        self.PG_PORT=5432
        self.PG_NAME="test_decimation"
        self.PG_TABLE = "pa"
        self.PG_COLUMN = "pa"

        self.db = connect(
                "postgresql://{0}:{1}@{2}:{3}/{4}"
                .format(self.PG_USER, self.PG_PASSWORD, self.PG_HOST,
                    self.PG_PORT, self.PG_NAME),
                cursor_factory=NamedTupleCursor,
                )

    def get_patch(self, id):
        sql = ("select pc_get(pc_explode({0}), 'x') as x"
                ", pc_get(pc_explode({0}), 'y') as y"
                ", pc_get(pc_explode({0}), 'z') as z"
                " from {1} where id = {2};"
        .format(self.PG_COLUMN, self.PG_TABLE, id))
        return self._query_asdict( sql )

    def get_patch_min(self, id):
        sql = ("select pc_patchmin({0}, 'x') as x"
                ", pc_patchmin({0}, 'y') as y"
                ", pc_patchmin({0}, 'z') as z"
                " from {1} where id = {2};"
        .format(self.PG_COLUMN, self.PG_TABLE, id))
        return self._query_asdict( sql )[0]

    def get_patch_max(self, id):
        sql = ("select pc_patchmax({0}, 'x') as x"
                ", pc_patchmax({0}, 'y') as y"
                ", pc_patchmax({0}, 'z') as z"
                " from {1} where id = {2};"
        .format(self.PG_COLUMN, self.PG_TABLE, id))
        return self._query_asdict( sql )[0]

    def _query(self, query, parameters=None):

        cur = self.db.cursor()
        cur.execute(query, parameters)
        if not cur.rowcount:
            return None
        for row in cur:
            yield row

    def _query_asdict(self, query, parameters=None):
        return [
            line._asdict()
            for line in self._query(query, parameters=parameters)
        ]

    def _query_aslist(self, query, parameters=None):
        return list(chain(*self._query(query, parameters=parameters)))
