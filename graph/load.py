from hashlib import sha256
from pathlib import Path
import pandas as pd
from .models import DataValidationError


def load(data_dir):
    frames, checksums = {}, {}
    for name in ('nodes', 'edges', 'transactions'):
        path = Path(data_dir) / f'{name}.parquet'
        try:
            raw = path.read_bytes()
            # Parse exactly the bytes whose checksum is recorded.
            from io import BytesIO
            frames[name] = pd.read_parquet(BytesIO(raw))
            checksums[path.name] = sha256(raw).hexdigest()
        except Exception as exc:
            raise DataValidationError(f'Не удалось прочитать {path.name}: {type(exc).__name__}',
                                      {'file': path.name}) from exc
    return frames['nodes'], frames['edges'], frames['transactions'], checksums
