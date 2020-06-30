#!/usr/bin/env python
import luigi
import yaml
import requests

from datetime import datetime

DEFAULT_PARAMS = {
    "url_list_src": (
        "https://gist.githubusercontent.com/mattfeng/" + 
        "4e38ec5973607d42dbee5b2d3be93048/raw/" + 
        "36de6abbc08e80602a77dc658dec96ebdf6892f0/track.yml"),
}

class GatherSitesTask(luigi.Task):
    """Gather the sites to scrape from an external resource.
    """
    url_list_src = luigi.Parameter(default=DEFAULT_PARAMS["url_list_src"])
    suffix       = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(
            "/tmp/scrape-{}/urls.yml".format(self.suffix)
            )

    def requires(self):
        pass

    def run(self):
        print(f"Getting URLs to scrape from {self.url_list_src}")
        resp = requests.get(self.url_list_src)
        print(resp.text)

        with self.output().open('w') as f:
            f.write(resp.text)
            f.write('\n')

class ScrapeSiteTask(luigi.Task):
    """Scrape an individual website for its HTML content.
    """
    url    = luigi.Parameter()
    name   = luigi.Parameter()
    suffix = luigi.Parameter()

    def requires(self):
        pass

    def output(self):
        return luigi.LocalTarget(
            "/tmp/scrape-{}/{}.html".format(self.suffix, self.name)
            )

    def run(self):
        resp = requests.get(self.url)
        with self.output().open("w") as f:
            f.write(resp.text)
            f.write('\n')
        print(f"Finished grabbing data from {self.url} ({self.name}).")
        
class ScrapeSitesTask(luigi.Task):
    output_suffix = datetime.now().isoformat()
    
    def requires(self):
        return GatherSitesTask(suffix=self.output_suffix)
    
    def run(self):
        with self.input().open() as f:
            data = yaml.load(f)
        
        for entry in data:
            url = entry["url"]
            name = entry["name"]

            yield ScrapeSiteTask(suffix=self.output_suffix, name=name, url=url)
        

