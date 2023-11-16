""" This module contains the CSVDataManager class which is responsible for handling the operations related
to reading and parsing CSV files. This includes loading data from a file, managing data frames, and providing
access to the data for visualization purposes. """
from typing import List, Optional, Dict, Union, Tuple
import datetime
import colorsys
import pathlib
import pandas as pd


class CSVDataManager:
    ''' Module for CSV file operations '''
    def __init__(self, filepath: str, prefix: Optional[str] = 'Truma_n_'):
        self._filepath: str = filepath
        self._prefix: str = prefix

        self.loaded = self._load_data()

        self._nr_of_data: int = len(self._dataframe.columns)

    def _load_data(self) -> Optional[pd.DataFrame]:
        """  Load and return data from a CSV file. """
        self._dataframe: pd.DataFrame = None
        try:
            self._dataframe = pd.read_csv(self._filepath, delimiter=';', quotechar='|')
            return True
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"The file {self._filepath} was not found.") from exc
        except pd.errors.EmptyDataError as exc:
            raise pd.errors.EmptyDataError(f"No columns to parse from file: {self._filepath}") from exc
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid file type: {pathlib.Path(self._filepath).suffix}") from exc
        except ValueError as exc:
            raise ValueError(f"Invalid file path or buffer object type: {type(self._filepath)}") from exc
        except TypeError as exc:
            raise TypeError("Missing 1 required positional argument: 'filepath") from exc
        except Exception as exc:
            raise Exception(f"An unexpected error occurred: {exc}") from exc

    def _validate_index(self, idx: int) -> None:
        if isinstance(idx, int) and (idx < 0 or self._nr_of_data <= idx):
            raise IndexError(f"Index '{idx}' out of range.")

    def _validate_header(self, hdr: int) -> None:
        if isinstance(hdr, str) and hdr not in self.header_list:
            raise ValueError(f"Header '{hdr}' not found")

    def _validate_input(self, idx: int = None, hdr: str = None) -> None:
        """ Validate the header or the index. """
        self._validate_index(idx)
        self._validate_header(hdr)

        if idx is None and hdr is None:
            raise ValueError("An index or header name must be provided.")
        elif idx is not None and hdr is not None:
            raise ValueError("Only one of index or header name should be provided.")
        elif hdr is None and not isinstance(idx, int):
            raise ValueError("Did you mean to provide the hdr? (hdr= )")
        elif idx is None and not isinstance(hdr, str):
            raise ValueError("Did you mean to provide the idx? (idx= )")

    def _get_data_by_header(self, header: str) -> Optional[pd.Series]:
        """ Get data for a specific header, handling the case where the header does not exist. """
        self._validate_header(header)
        return self._dataframe.get(header)

    def _get_data_by_index(self, index: int) -> Optional[pd.Index]:
        """ Get data for a specific index. """
        self._validate_index(index)
        return self._dataframe.iloc[:, index]

    def _get_raw_data(self, idx: int = None, hdr: str = None) -> Optional[pd.Index] | Optional[pd.Series]:
        self._validate_input(idx, hdr)

        data = self._get_data_by_index(idx) if idx is not None else self._get_data_by_header(hdr)

        return data

    @staticmethod
    def _parse_time(raw_time: float) -> Tuple[float, float, float]:
        """Parse time data from timestamp or date-time format to hours, minutes, seconds."""
        raw_time = format(raw_time, '.3f')
        try:
            parsed_time = str(datetime.datetime.utcfromtimestamp(int(str(raw_time).replace('.', '')) / 1e3)).split()[1].split(':')
        except ValueError:
            parsed_time = str(raw_time).split()[1].split(':')

        return tuple(map(float, parsed_time))

    def _calculate_time_in_seconds(self, raw_time: float, time_offset: List[float]) -> float:
        """Convert parsed time to total seconds."""
        hr, _min, sec = self._parse_time(raw_time)
        return round((hr - time_offset[0]) * 3600 + (_min - time_offset[1]) * 60 + sec - time_offset[2], 3)

    @property
    def header_list(self) -> List[str]:
        """ Get the list of headers from the CSV file. """
        return self._dataframe.columns.tolist()

    @property
    def index_list(self) -> List[str]:
        """ Get the list of headers from the CSV file. """
        return list(range(len(self.header_list)))

    @property
    def headers_mapping(self) -> Optional[Dict[str, List[Union[str, int]]]]:
        """ Create a mapping of header names to their indices with groupheader and header keys. """
        hdr_mapping: Dict[str, List[Union[str, int]]] = {}

        for idx, header in enumerate(self.header_list):
            strpped_header = header.replace(self._prefix, '') if self._prefix in header else header
            group_header, header_key = strpped_header.split('::') if '::' in strpped_header else (None, strpped_header)
            hdr_mapping.setdefault(group_header, []).append([header_key, idx])

        return hdr_mapping

    @property
    def const_data_index_list(self) -> Optional[List[int]]:
        """ Get the list of constant column indices from the CSV file. """
        const_data_idx_list: List[int] = []

        for idx, column in enumerate(self._dataframe.columns):
            datafram_col = self._dataframe[column]
            # All values are equal to the first value
            if (datafram_col == datafram_col.iloc[0]).all():
                # Store the index of the constant data
                const_data_idx_list.append(idx)

        return const_data_idx_list

    @property
    def const_zero_data_index_list(self) -> Optional[List[int]]:
        """ Get the list of constant zero column indices from the CSV file. """
        const_zero_data_idx_list: List[int] = []

        for idx, column in enumerate(self._dataframe.columns):
            if (self._dataframe[column] == 0).all():
                # Store the index of the constant zero data
                const_zero_data_idx_list.append(idx)

        return const_zero_data_idx_list

    @property
    def varying_data_index_list(self) -> List[int]:
        """ Get the indices of constant zero data. """
        return [set(self.const_data_index_list) ^ set(self.index_list)]

    @property
    def time_data_list(self) -> List[float]:
        """Extract time data from the CSV and convert it to seconds."""
        time_data_list: List[float] = [0.0]

        data = self.get_data(hdr='time index')
        time_offset = self._parse_time(data[0])
        for row in data[1:]:
            time_data_list.append(self._calculate_time_in_seconds(row, time_offset))

        return time_data_list

    def get_header(self, index: int) -> str:
        """ Get the header of the corresponding index from the CSV file. """
        self._validate_index(index)
        return str(self._dataframe.columns[index])

    def get_index(self, header: str) -> int:
        """ Get the index of the corresponding header from the CSV file. """
        self._validate_header(header)
        return int(self._dataframe.columns.get_loc(header))

    def get_data(self, idx: int = None, hdr: str = None) -> List[float]:
        ''' Get the data from the CSV file as a list of floats. '''
        data = self._get_raw_data(idx, hdr)
        return [float(value) for value in data]

    def get_data_extrema(self, idx: Optional[int] = None, hdr: Optional[str] = None) -> Tuple[float, float]:
        """ Calculate the maxima and minima of the data for either a given index or header.
        Adds a buffer to avoid the data being at the very top or bottom of the chart.
        For a constant signal, especially zero, provides a default small range around the value. """
        data = self._get_raw_data(idx, hdr)

        # Calculate extrema
        min_val, max_val = min(data), max(data)

        # Handle constant signal, especially zero
        if min_val == max_val:
            # Provide a range around the constant value
            return min_val - 1.0, max_val + 1.0

        buffer = abs(0.05 * (max_val - min_val))
        return round(min_val - buffer, 3), round(max_val + buffer, 3)

    def get_unique_color_code(self, index: int) -> int:
        """Calculate color based on the subheading number using HSL."""
        self._validate_index(index)
        # Calculate a hue value using modulo to wrap around after reaching 1.0.
        # The larger the denominator, the more distinct colors for consecutive values.
        color_factor = 0xFFFFFF / self._nr_of_data
        hue = (int(index) * color_factor) % self._nr_of_data / self._nr_of_data
        saturation, lightness = 0.9, 0.6
        # TODO: try this instead:
        # TODO: golden_ratio_conjugate = 0.618033988749895
        # TODO: hue = ((idx * golden_ratio_conjugate) % 1)
        # TODO: or:
        # TODO: hue = ((idx / self.__nr_of_data) % 1)

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

        # Convert RGB values from 0-1 range to 0-255 and then to hexadecimal
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


if __name__ == '__main__':
    csv_manager = CSVDataManager('resources/TelemetryUI_log_2023_11_14_14_34_10_good.csv')

    print(f"Header map: {csv_manager.headers_mapping}")
    print('#===============================================#')
    print(f"Headers: {csv_manager.header_list}")
    print('#===============================================#')
    print(f"Indices: {csv_manager.index_list}")
    print('#===============================================#')
    print(f"Varying data indices: {csv_manager.varying_data_index_list}")
    print('#===============================================#')
    print(f"Const. data indices: {csv_manager.const_data_index_list}")
    print('#===============================================#')
    print(f"Const. zero data indices: {csv_manager.const_zero_data_index_list}")
    print('#===============================================#')
    print(f"Calculated time: {csv_manager.time_data_list}")
    print('#===============================================#')
    print('#===============================================#')
    print('#===============================================#')
    label = csv_manager.header_list[43]
    print(f"Label: '{label}'")
    print('#===============================================#')
    print(f"Data: {csv_manager.get_data(hdr='Truma_n_AmcuDebugData::operationTime')}")
    print('#===============================================#')
    print(f"Colorcode from index: {csv_manager.get_unique_color_code(csv_manager.get_index('Truma_n_AmcuDebugData::operationTime'))}")
    print('#===============================================#')
    print(f"Data extrema from index: {csv_manager.get_data_extrema(csv_manager.get_index('Truma_n_AmcuDebugData::operationTime'))}")
    print('#===============================================#')
    print(f"Data extrema from header: {csv_manager.get_data_extrema(hdr=csv_manager.get_header(43))}")
