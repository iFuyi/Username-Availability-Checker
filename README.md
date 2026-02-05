# Handle Scout

Handle Scout is a small FastAPI app that checks whether a username is likely
available on several popular platforms. Results are best-effort and may be
inaccurate for platforms that block or challenge automated requests.

## Quick start

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:8000 in your browser.

## Supported platforms

- GitHub
- Reddit
- TikTok (best-effort, may return unknown)
- X (Twitter) (best-effort, may return unknown)
- Discord (reported as unknown)

## API example

Request:

```
GET /api/check?username=jonasdev
```

Response:

```json
{
	"username": "jonasdev",
	"timestamp": "2026-02-06T12:00:00Z",
	"results": [
		{
			"platform": "GitHub",
			"url": "https://github.com/jonasdev",
			"status": "available",
			"http_status": 404,
			"reason": "Profile returns 404 => likely available"
		}
	],
	"suggestions": ["jonasdevhq", "jonasdev_", "jonas_dev"]
}
```

## How it works

- Uses public profile URLs and HTTP status checks (no API keys)
- Runs checks concurrently with `httpx`
- Adds timeouts and a basic per-IP rate limit

## Add a new platform

Edit [platforms.py](platforms.py) and add a new entry to `PLATFORMS`.

Checklist:

- Choose a profile URL template
- Decide which status codes indicate availability
- Add any special headers
- Keep logic simple and explainable

## Contributing

Pull requests are welcome. Please:

- Keep checks best-effort and lightweight
- Avoid API keys or heavy scraping
- Add clear reasons for `unknown` results

## License

MIT
