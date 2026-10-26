from pydantic import BaseModel
from pydantic import BaseModel

class MeterSummary(BaseModel):
    meter_id: str
    serial_no: str
    make: str
    phase_type: str
    install_status: str
    dt_code: str

class MeterSearchResponse(BaseModel):
    data: list[MeterSummary]
    total: int
    page: int
    page_size: int

class MeterLocation(BaseModel):
    latitude: float
    longitude: float

class EnergyReading(BaseModel):
    timestamp: str
    kwh: float
    kvah: float
    volt_r: float

class MeterEnergyResponse(BaseModel):
    data: list[EnergyReading]
