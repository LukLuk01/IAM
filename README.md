IAM Demo – Keycloak + OIDC

Konfiguracja
cp .env.example .env

Uzupełnij:

OIDC_CLIENT_SECRET=

skonfiguruj Keyloak

docker compose up --build -d


Usługa	URL
Keycloak	http://localhost:8080
OIDC App	http://localhost:5000
SAML App	http://localhost:5001


SAML - > TBC


Admin (Keycloak)
login: admin
hasło: admin
User
login: test
hasło: test123 
