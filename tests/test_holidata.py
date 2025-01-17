import pytest
from snapshottest.file import FileSnapshot
from snapshottest.formatter import Formatter

from holidata import Locale
from tests import HOLIDATA_YEAR_MAX


@pytest.fixture(params=range(2011, HOLIDATA_YEAR_MAX))
def year(request):
    return request.param


@pytest.fixture(params=Locale.plugins)
def locale(request, year):
    return request.param(year)


def test_holidata_produces_holidays_for_locale_and_year(snapshot, tmpdir, locale):
    temp_file = tmpdir.join('{}.{}.py'.format(locale.locale, locale.year))

    export_data = [h.as_dict() for h in locale.holidays]
    export_data.sort(key=lambda x: x['date'])
    temp_file.write(Formatter().format(export_data, 0))

    snapshot.assert_match(FileSnapshot(str(temp_file)))
