from pathlib import Path

import pytest
import quiz

import yelp

_ = quiz.SELECTOR

TOKEN = Path('~/.creds/yelp.txt').expanduser().read_text().strip()


@pytest.fixture(scope='session')
def execute():
    return yelp.executor(auth=TOKEN)


def test_module():
    issubclass(yelp.Business, quiz.Object)


def test_simple(execute):

    query = yelp.query[
        _
        ('delft_places').search(location='Delft')[
            _
            .total
            .business[
                _
                .name
                .rating
                .price
                .hours[
                    _
                    .hours_type
                    .is_open_now
                ]
            ]
        ]
        .business(id='garaje-san-francisco')[
            _
            .hours[
                _
                .open[
                    _
                    .is_overnight
                    .end
                    .start
                    .day
                ]
            ]
        ]
    ]

    result = execute(query)
    assert result.delft_places.total > 4
    assert result.delft_places.business[0].hours[0].hours_type == 'REGULAR'


def test_get_schema():
    schema = quiz.Schema.from_url(yelp.URL, auth=yelp.auth_factory(TOKEN))
    assert isinstance(schema, quiz.Schema)
