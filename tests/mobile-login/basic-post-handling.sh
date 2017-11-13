!#/bin/bash

echo ""
echo "ONLY USED TO TEST BASIC POST HANDLING AND IS NOT AN ACCEPTANCE TEST"
echo ""
echo "Generates random POST request to mobile login handling"
echo ""
echo "Should return JSON:"
echo "  200: Created new account"
echo "  403: Invalid email or password"
echo "  200: Login successful"

RANDOM="$((1 + RANDOM % 10000))"
TEMP=$RANDOM
echo ""
echo "========= RESULTS =========="
curl -H "Content-Type: application/json" -X POST -d '{"email":"'$TEMP'","password":"'$TEMP'"}' http://localhost/mobilelogin/
echo ""
curl -H "Content-Type: application/json" -X POST -d '{"email":"'$TEMP'","password":"'$TEMP'X"}' http://localhost/mobilelogin/
echo ""
curl -H "Content-Type: application/json" -X POST -d '{"email":"'$TEMP'","password":"'$TEMP'"}' http://localhost/mobilelogin/
echo ""
echo ""
