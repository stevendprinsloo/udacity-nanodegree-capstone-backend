#!/bin/bash

export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/casting_agency"
export AUTH0_DOMAIN='dev-ciko6qxd.us.auth0.com'
export ALGORITHMS=`['RS256']`
export API_AUDIENCE='casting_agency'

echo "setup.sh script executed successfully!"
