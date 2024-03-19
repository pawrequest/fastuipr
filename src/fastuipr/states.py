import base64
import typing as _t

import pydantic as _p

from . import types_


class BaseUIState(_p.BaseModel):
    alert_dict: types_.AlertDict | None = None  # msg -> type

    def update_get_query64(self, **kwargs) -> dict[str, str]:
        """returns {'update': updated jsonb64}"""
        update = self.model_copy(update=kwargs)
        return update.base64_query('update')

    def base64_query(self, query_key='state') -> dict[str, str]:
        return {f'{query_key}_64': self.model_dump_64()}

    def model_dump_64(self):
        state_ = self.model_dump_json()
        return base64.urlsafe_b64encode(state_.encode()).decode()

    @classmethod
    def model_validate_64(cls, state_64: str) -> _t.Self:
        try:
            state_ = base64.urlsafe_b64decode(state_64).decode()
            return cls.model_validate_json(state_)
        except _p.ValidationError as e:
            raise ValueError(f'{state_64=} is not a valid base64 encoded {cls.__name__} - {e}')

    def update_dump_64(self, **kwargs) -> str:
        updated = self.model_copy(update=kwargs)
        return updated.model_dump_64()

    def update_dump_64_o(self, updater: 'BaseUIState') -> str:
        updated = self.model_copy(update=updater.model_dump(exclude_none=True))
        return updated.model_dump_64()

    def get_updated(self, updater: 'BaseUIState') -> _t.Self:
        """return a new BookingStateUpdate with the values of other merged into self."""
        up_dict = {update: getattr(updater, update) for update in updater.model_fields_set}
        return self.model_validate(self.model_copy(update=up_dict))
