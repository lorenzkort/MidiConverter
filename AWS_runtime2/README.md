# MidiConverter

docker run -p 9000:8080 -v ~/.aws:/root/.aws midi-converter
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"file_id":"00caef2d-0c97-47d2-9f09-05c92162f465-1.mp3"}'