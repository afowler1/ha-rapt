"""Constants for the RAPT integration."""

DOMAIN = "rapt"

# API Constants
API_BASE_URL = "https://api.rapt.io/api"
API_AUTH_URL = "https://id.rapt.io/connect/token"
API_CONTROLLERS_ENDPOINT = "/TemperatureControllers/GetTemperatureControllers"
API_HYDROMETERS_ENDPOINT = "/Hydrometers/GetHydrometers"
API_FERMENTATION_CHAMBERS_ENDPOINT = "/FermentationChambers/GetFermentationChambers"
API_BREWZILLAS_ENDPOINT = "/BrewZillas/GetBrewZillas"

# Update intervals
UPDATE_INTERVAL_SECONDS = 60

# Configuration constants
CONF_USERNAME = "username"
CONF_API_SECRET = "api_secret"