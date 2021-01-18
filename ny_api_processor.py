import psycopg2
from collections import OrderedDict


from api_processors.api_processor import APIProcessor


class NYAPIProcessor(APIProcessor):

    def __init__(self):
        super().__init__()
        self.url = "https://api.nytimes.com/svc/news/v3/content/all/all.json"
        self.api_key = "6LWMg0c19nLU7dKwBR6QRXQ5A6elwqmp"
        self.news_fields = ["slug_name", "section", "subsection", "title",
                            "abstract", "url", "source", "published_date",
                            "multimedia", "des_facet", "per_facet",
                            "org_facet", "geo_facet", "ttl_facet",
                            "topic_facet", "porg_facet"]
        self.cor_table_field = ["nyt", "title", "abstract", "slug_name",
                                "published_date", "url", "source", "multimedia"]

    def _clean_data(self, raw_data):
        """
        Will get explicit data from API (list of dicts), remove unnecessary
        fields from each entry, and prepare a list of tuples for saving
        to the DB.
        Values order for tuple: "nyt", title, abstract, slug_name,
        published_date, url, internal_source, media_url.
        :param raw_data:
        :return: reordered_data
        """
        # TODO: update in accordance with docstring
        clean_data = list()
        raw_news = raw_data['results']
        if not raw_news:
            raise RuntimeError("No news in received data")
        for item in raw_news:
            cleaned_data = {k: v for k, v in item.items()
                            if k in self.news_fields}
            clean_data.append(cleaned_data)


        corrected_data =list()
        for item in clean_data:
            cor_data = {k: v for k, v in item.items() if k in self.cor_table_field}
            corrected_data.append(cor_data)


        reordered_data = list()
        for item in corrected_data:
            reorder_data = sorted(item.items())
            reordered_data.append(reorder_data)


        return reordered_data


    def _save_data(self, data_to_save):
        query = """
        INSERT INTO news (
            source_api,
            title,
            abstract,
            slug_name,
            published_date,
            url,
            internal_source,
            media_url
        )
        VALUES (%s);
        """
        raise NotImplementedError

if __name__ == '__main__':
    t = NYAPIProcessor()
    t.refresh_data()
