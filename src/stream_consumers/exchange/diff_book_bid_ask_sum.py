from typing import Any
from src.helpers.decorators import consumer_source
from src.stream_consumers.exchange_stream_consumer import ExchangeStreamConsumer
from src.util import get_logger
import pandas as pd
from rx.subject import Subject # type: ignore

@consumer_source(stream_name='diff_book_depth')
class DiffBookBidAskSum(ExchangeStreamConsumer):
    """
     Need a reference to the window to access the data frames
     https://binance-docs.github.io/apidocs/futures/en/#diff-book-depth-streams
    """
    col_mapping = {
        'e': 'event_type',
        'E': 'event_timestamp',
        'T': 'timestamp',
        's': 'symbol',
        'U': 'first_update_id_event',
        'u': 'final_update_id_event',
        'pu': 'previous_final_update_id_event',
        'b': 'total_bid_quantity',  # originally Bids to be updated
        'a': 'total_ask_quantity'  # originally Asks to be updated
    }

    def __init__(self, primary: Subject):
        super().__init__(primary, self.col_mapping)
        super().subscribe({'speed': '500'})
        self.logger = get_logger(self)

    def transform_message_dict(self, input_dict: Any) -> dict[str, str | int] | None:
        input_dict["b"] = sum(float(x[1]) for x in input_dict["b"])
        input_dict["a"] = sum(float(x[1]) for x in input_dict["a"])
        return input_dict

    # FIXME: there are ordering checks that need to be done as described in the docs
    def diff_book_resample(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This consumer receives a rows ever 500ms.  We want to resample the data at 30s intervals.
        """
        df_copy = df.drop(columns=["event_type", 'event_timestamp', "first_update_id_event",
                "final_update_id_event", "previous_final_update_id_event"]).copy()
        self.logger.info(f"diff_book_resample ~ resampled: df_copy.columns: {df_copy.columns}")
        resampled = df_copy.resample('30s').sum() # type: ignore
        self.logger.info("diff_book_resample ~ resampled", type(resampled))
        return resampled
