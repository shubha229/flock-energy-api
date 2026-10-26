# Urja Meter Ops — Protocol Notes

## 1. Overview

Urja Meter Ops is a web portal for accessing smart-meter information. The portal was examined using its interface and browser Developer Tools to identify how it retrieves meter data.

The investigation covered meter search, meter details, geographic coordinates, energy readings, authentication, and the electricity distribution network hierarchy.

All portal operations were read-only.

## 2. Authentication

Authentication is required to access meter information.

### Observed behavior

- The login endpoint is `POST /login`.
- The request uses form data containing `email` and `password`.
- Required headers include `Accept: application/json`, `Origin`, `Referer`, and `X-Sveltekit-Action: true`.
- Requests without the expected headers returned a cross-site form submission error.
- With valid credentials and the expected headers, the portal returned a `303` redirect to `/meters`.
- A session cookie was established for subsequent authenticated requests.

The Python client uses `requests.Session()` to maintain the session across requests.

### Limitations

Session expiration and automatic reauthentication have not been fully tested.

Credentials and session cookies must remain private and must never be committed to the repository.

## 3. Meter Listing and Search

The portal provides a searchable meter listing. During the investigation, it displayed 403 meters. This count reflects the dataset at the time of inspection and may change.

### Observed request

`GET /portal/meters/search?q=&page=1`

The request returned `200 OK` with a JSON response containing:

- `data`: meter records for the requested page
- `total`: total number of matching records
- `page`: current page number
- `pageSize`: page size

The initial request used an empty search query and page number `1`.

### Observed meter fields

The records included:

- `meterId`
- `serialNo`
- `make`
- `phaseType`
- `installStatus`
- `dtCode`

For example, meter `J100000` had serial number `SE33962`, make `HPL`, phase type `single`, installation status `Decommissioned`, and distribution transformer code `DT-001`.

The portal interface supports searching by meter number or serial number. Partial-match behavior and other search rules require further testing.

## 4. Meter Details and Network Hierarchy

Opening a meter displays its detailed information.

For meter `J100000`, the portal showed:

- Meter ID: `J100000`
- Serial number: `SE33962`
- Make: `HPL`
- Phase type: `single`
- Installation status: `Decommissioned`
- Installation type: `Whole Current`

The page also displayed the meter's position in the electricity distribution network:

`Jaipur Zone 1 (Z-01) → Circle 1 (C-01) → Division 1 (D-01) → Subdivision 1 (SD-01) → Substation 1 (SS-01) → Feeder 1 (F-001) → Malviya Nagar DT 1 (DT-001)`

A dedicated endpoint for retrieving the complete hierarchy has not been confirmed. Exposing the hierarchy through the API is outside the current implementation.

## 5. Geographic Data

Opening a meter triggered a request for its geographic information.

### Observed request

- Method: `GET`
- Path: `/portal/meters/J100000/geo`
- Status: `200 OK`
- Response format: JSON

The response contained a `data` object with `latitude` and `longitude` fields. For the inspected meter, both coordinates were returned as strings.

The meter ID is included in the request path, and the FastAPI service exposes this information through its meter location endpoint.

Behavior for meters without geographic information has not been fully tested.

## 6. Energy Data

Opening a meter also triggered a request for its energy readings.

### Observed request

- Method: `GET`
- Path: `/portal/meters/J100000/energy`
- Status: `200 OK`
- Response format: JSON

The response contained a `data` array with fields including:

- `timestamp`
- `kwh`
- `kvah`
- `voltR`

The inspected response contained timestamps approximately 30 minutes apart. This indicates half-hourly readings for that response, but the interval has not been verified across all meters or time ranges.

The full historical range, number of readings, supported date filters, measurement units, and handling of missing readings require further investigation.

## 7. SvelteKit Page Data

When a meter details page was opened, the portal also requested SvelteKit page data:

`GET /meters/J100000/__data.json?x-sveltekit-invalidated=001`

The request returned `200 OK` with serialized page data.

Since dedicated JSON endpoints were available for meter search, geographic coordinates, and energy readings, the implementation uses those endpoints for the supported operations. The page-data response may be useful for investigating additional meter details or the network hierarchy.

## 8. Observed Portal Requests

| Request | Method | Observed result | Purpose |
|---|---|---|---|
| `/login` | POST | Redirect after successful login | Authentication |
| `/portal/meters/search?q=&page=1` | GET | `200 OK` | Meter search and listing |
| `/portal/meters/J100000/geo` | GET | `200 OK` | Geographic coordinates |
| `/portal/meters/J100000/energy` | GET | `200 OK` | Energy readings |
| `/meters/J100000/__data.json?x-sveltekit-invalidated=001` | GET | `200 OK` | SvelteKit page data |

These results reflect requests captured during the investigation. Responses may differ for other meter IDs or session conditions.

## 9. API Design

The API uses FastAPI as a separate service in front of the existing portal.

The request flow is:

1. A client sends a request to the FastAPI service.
2. The portal client authenticates when necessary.
3. The portal client requests the relevant data endpoint.
4. The service validates and structures the response using its data models.
5. The service returns JSON to the client.

The implementation supports meter search, location, and energy readings. Other portal features are outside the current scope.

The existing portal remains the source of truth, and the service does not intentionally modify portal data.

## 10. Error Handling and Limitations

The API handles portal request failures and maps upstream errors to API responses. Tests have covered invalid meter IDs and invalid page input.

Additional testing is required for:

- Expired sessions and reauthentication
- Portal timeouts and server errors
- Malformed or unexpected JSON responses
- Meters without geographic data
- Meters without energy readings
- Search and pagination edge cases

The existing tests do not establish that every upstream failure scenario has been covered.

## 11. Security

The portal was accessed through authenticated, read-only requests.

The implementation follows these precautions:

- Credentials are supplied through environment variables.
- Real credentials are excluded from source control.
- Session cookies and authentication details are not returned to API consumers.
- Portal requests use timeouts.
- The repository contains `.env.example` rather than the real `.env` file.

## 12. Remaining Work

The following improvements remain:

1. Test session expiration and reauthentication.
2. Expand tests for upstream failures and unexpected response formats.
3. Investigate how to retrieve the complete network hierarchy.
4. Test search behavior for meter IDs, serial numbers, partial matches, and missing results.
5. Examine historical energy coverage and supported date filters.
6. Evaluate caching and structured logging.

## 13. Conclusion

The investigation identified the JSON requests used by the Urja Meter Ops portal to retrieve meter information.

Using the observed authentication flow and dedicated data endpoints, the project provides a FastAPI service for meter search, geographic coordinates, and energy readings. The service keeps the existing portal as its data source and provides a separate interface for accessing the supported information.

Network hierarchy support, session renewal, and additional failure scenarios remain areas for further development.