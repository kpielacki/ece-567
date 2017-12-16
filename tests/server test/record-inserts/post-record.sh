#!/bin/bash

echo ""
echo "Used to test POST data upload to tables user_location and user_steps"
echo ""
echo "Should return JSON upon first success:"
echo "  200: Record Insert Successful"
echo "  200: Record Insert Successful"
echo "Should return JSON upon after record insert failing unique constraint:"
echo "  400: Malformed Data Entered"
echo "  400: Malformed Data Entered"

echo ""
echo "========= RESULTS =========="
curl -H "Content-Type: application/json" -X POST -d  "$(< loc_records.json)" http://localhost/mobile/uploadtable/
echo ""

curl -H "Content-Type: application/json" -X POST -d  "$(< step_records.json)" http://localhost/mobile/uploadtable/
echo ""
