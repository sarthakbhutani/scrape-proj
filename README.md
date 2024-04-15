# Installation Steps - 

- Install redis, python
- Start redis-server
- create a virtual environment (if needed)
- do ```pip3 install -r requirements.txt```
- to start the server ```uvicorn app.server:app --reload --port 9200```

------

## CURL for login - 
```
curl 'http://localhost:9200/atlys/token' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' \
  -H 'Authorization: Basic Og==' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Origin: http://localhost:9200' \
  -H 'Referer: http://localhost:9200/docs' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw 'grant_type=password&username=atlys_admin&password=atlys_admin_password'
```

## CURL for scraping - 
```
curl --location 'localhost:9200/atlys/scrape' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdGx5c19hZG1pbiIsImV4cCI6MjA3MzIxOTU0M30.H6GSvkRjM11wS790R0wpw8SK3orrXHwI7Z_rB3yfKlQ' \
--header 'request_id: abcd' \
--header 'Content-Type: application/json' \
--data '{
    "url":"https://dentalstall.com/shop/page/",
    "page":3
}'
```
