class Mixin:
    def search_points(self, point_ids: dict, collection_name: str,):
        points = self._client.retrieve(
            collection_name=collection_name,
            ids=point_ids,
        )

        return points