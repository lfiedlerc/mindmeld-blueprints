import luigi

from .extract_ids import ExtractMovieIDs
from .extract_ids import ExtractTVIDs
from .extract_details import ExtractMovieDetails
from .extract_details import ExtractTVDetails
from .extract_credits import ExtractMovieCredits
from .extract_credits import ExtractTVCredits
from .extract_episodes import GetEpisodes


class ExtractIDs(luigi.WrapperTask):
    def requires(self):
        return [ExtractMovieIDs(), ExtractTVIDs()]


class ExtractDetails(luigi.WrapperTask):
    def requires(self):
        return ExtractIDs()

    def run(self):
        yield ExtractMovieDetails()
        yield ExtractTVDetails()


class ExtractCredits(luigi.WrapperTask):
    def requires(self):
        return ExtractIDs()

    def run(self):
        yield ExtractMovieCredits()
        yield ExtractTVCredits()


class ExtractEpisodes(luigi.WrapperTask):
    def requires(self):
        return ExtractDetails()

    def run(self):
        yield GetEpisodes()


class ExtractTMDB(luigi.WrapperTask):
    def requires(self):
        return [ExtractDetails(), ExtractCredits()]


if __name__ == '__main__':
    luigi.run()
