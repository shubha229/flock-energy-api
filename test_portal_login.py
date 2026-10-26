
from app.client import PortalClient


def main():
    client = PortalClient()

    try:
        client.login()
        print("Portal login succeeded.")

        response = client.get(
            "/portal/meters/search",
            params={"q": "", "page": 1},
        )

        print("Meter search status:", response.status_code)

        result = response.json()
        print("Response keys:", list(result.keys()))

        data = result.get("data", [])
        print("Meters returned:", len(data))

        if data:
            print("First meter:", data[0])

    except Exception as exc:
        print("Portal test failed:", exc)

    finally:
        client.close()


if __name__ == "__main__":
    main()
