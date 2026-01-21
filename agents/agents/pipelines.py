import os
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter, CsvItemExporter


class MultiExportPipeline:
    """
    Exports items to both JSONL and CSV in a /exports folder.
    JSONL is great for large data and streaming.
    CSV is what most Upwork clients want.
    """

    def open_spider(self, spider):
        os.makedirs("exports", exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.json_path = f"exports/agents_{ts}.jsonl"
        self.csv_path = f"exports/agents_{ts}.csv"

        self.json_file = open(self.json_path, "wb")
        self.csv_file = open(self.csv_path, "wb")

        self.json_exporter = JsonLinesItemExporter(self.json_file, encoding="utf-8", ensure_ascii=False)
        self.csv_exporter = CsvItemExporter(self.csv_file, encoding="utf-8")

        self.json_exporter.start_exporting()
        self.csv_exporter.start_exporting()

    def close_spider(self, spider):
        self.json_exporter.finish_exporting()
        self.csv_exporter.finish_exporting()

        self.json_file.close()
        self.csv_file.close()

        spider.logger.info(f"Exported JSONL: {self.json_path}")
        spider.logger.info(f"Exported CSV:   {self.csv_path}")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.json_exporter.export_item(adapter.asdict())
        self.csv_exporter.export_item(adapter.asdict())
        return item

