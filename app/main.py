
from fastapi import FastAPI, HTTPException, Query

from app.client import PortalClient, PortalError
from app.models import MeterEnergyResponse, MeterSearchResponse


app = FastAPI(
    title="Urja Meter Ops API",
    description="A clean API over the Urja Meter Ops portal.",
    version="1.0.0",
)


def portal_error_response(exc: PortalError, meter_id: str | None = None):
    """Convert portal errors into appropriate API responses."""

    if exc.status_code == 404:
        detail = (
            f"Meter '{meter_id}' was not found."
            if meter_id
            else "The requested portal resource was not found."
        )
        raise HTTPException(status_code=404, detail=detail) from exc

    raise HTTPException(
        status_code=502,
        detail="The meter portal request failed.",
    ) from exc


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "Urja Meter Ops API",
    }


@app.get(
    "/meters",
    response_model=MeterSearchResponse,
    tags=["Meters"],
)
def search_meters(
    q: str = Query(
        default="",
        description="Search by meter ID or serial number",
    ),
    page: int = Query(default=1, ge=1),
):
    client = PortalClient()

    try:
        response = client.get(
            "/portal/meters/search",
            params={"q": q, "page": page},
        )
        result = response.json()

        meters = [
            {
                "meter_id": meter["meterId"],
                "serial_no": meter["serialNo"],
                "make": meter["make"],
                "phase_type": meter["phaseType"],
                "install_status": meter["installStatus"],
                "dt_code": meter["dtCode"],
            }
            for meter in result["data"]
        ]

        return {
            "data": meters,
            "total": result["total"],
            "page": result["page"],
            "page_size": result["pageSize"],
        }

    except PortalError as exc:
        portal_error_response(exc)

    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The meter portal returned an unexpected response.",
        ) from exc

    finally:
        client.close()


@app.get("/meters/{meter_id}/location", tags=["Meters"])
def get_meter_location(meter_id: str):
    client = PortalClient()

    try:
        response = client.get(f"/portal/meters/{meter_id}/geo")
        result = response.json()
        location = result["data"]

        return {
            "meter_id": meter_id,
            "latitude": float(location["latitude"]),
            "longitude": float(location["longitude"]),
        }

    except PortalError as exc:
        portal_error_response(exc, meter_id)

    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The portal returned an unexpected location response.",
        ) from exc

    finally:
        client.close()


@app.get(
    "/meters/{meter_id}/energy",
    response_model=MeterEnergyResponse,
    tags=["Meters"],
)
def get_meter_energy(meter_id: str):
    client = PortalClient()

    try:
        response = client.get(f"/portal/meters/{meter_id}/energy")
        result = response.json()

        readings = [
            {
                "timestamp": reading["timestamp"],
                "kwh": reading["kwh"],
                "kvah": reading["kvah"],
                "volt_r": reading["voltR"],
            }
            for reading in result["data"]
        ]

        return {"data": readings}

    except PortalError as exc:
        portal_error_response(exc, meter_id)

    except (ValueError, KeyError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The portal returned an unexpected energy response.",
        ) from exc

    finally:
        client.close()
