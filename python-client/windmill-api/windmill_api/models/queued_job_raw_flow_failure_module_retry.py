from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast
from ..types import UNSET, Unset
from typing import Dict

if TYPE_CHECKING:
  from ..models.queued_job_raw_flow_failure_module_retry_exponential import QueuedJobRawFlowFailureModuleRetryExponential
  from ..models.queued_job_raw_flow_failure_module_retry_constant import QueuedJobRawFlowFailureModuleRetryConstant





T = TypeVar("T", bound="QueuedJobRawFlowFailureModuleRetry")


@_attrs_define
class QueuedJobRawFlowFailureModuleRetry:
    """ 
        Attributes:
            constant (Union[Unset, QueuedJobRawFlowFailureModuleRetryConstant]):
            exponential (Union[Unset, QueuedJobRawFlowFailureModuleRetryExponential]):
     """

    constant: Union[Unset, 'QueuedJobRawFlowFailureModuleRetryConstant'] = UNSET
    exponential: Union[Unset, 'QueuedJobRawFlowFailureModuleRetryExponential'] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.queued_job_raw_flow_failure_module_retry_exponential import QueuedJobRawFlowFailureModuleRetryExponential
        from ..models.queued_job_raw_flow_failure_module_retry_constant import QueuedJobRawFlowFailureModuleRetryConstant
        constant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constant, Unset):
            constant = self.constant.to_dict()

        exponential: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exponential, Unset):
            exponential = self.exponential.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if constant is not UNSET:
            field_dict["constant"] = constant
        if exponential is not UNSET:
            field_dict["exponential"] = exponential

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.queued_job_raw_flow_failure_module_retry_exponential import QueuedJobRawFlowFailureModuleRetryExponential
        from ..models.queued_job_raw_flow_failure_module_retry_constant import QueuedJobRawFlowFailureModuleRetryConstant
        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, QueuedJobRawFlowFailureModuleRetryConstant]
        if isinstance(_constant,  Unset):
            constant = UNSET
        else:
            constant = QueuedJobRawFlowFailureModuleRetryConstant.from_dict(_constant)




        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, QueuedJobRawFlowFailureModuleRetryExponential]
        if isinstance(_exponential,  Unset):
            exponential = UNSET
        else:
            exponential = QueuedJobRawFlowFailureModuleRetryExponential.from_dict(_exponential)




        queued_job_raw_flow_failure_module_retry = cls(
            constant=constant,
            exponential=exponential,
        )

        queued_job_raw_flow_failure_module_retry.additional_properties = d
        return queued_job_raw_flow_failure_module_retry

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties