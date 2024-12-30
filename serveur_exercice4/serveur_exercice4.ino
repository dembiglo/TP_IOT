#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// Configuration WiFi
const char* ssid = "Gad";
const char* password = "Gadou242@";

// URL du serveur FastAPI
const char* serverUrl = "http://192.168.50.74:8000/api/capteur";

// Configuration du capteur DHT
#define DHTPIN D3 // Broche où le capteur est connecté
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient client; // Initialisation de l'objet WiFiClient

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Connexion au WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connexion WiFi...");
  }
  Serial.println("WiFi connecté !");
  dht.begin();
}

void loop() {
  // Vérification de la connexion WiFi
  if (WiFi.status() == WL_CONNECTED) {
    float temperature = dht.readTemperature();
    if (isnan(temperature)) {
      Serial.println("Erreur de lecture du capteur !");
      return;
    }

    // Envoi des données au serveur
    HTTPClient http;
    http.begin(client, serverUrl); // Utilisation de WiFiClient avec HTTPClient
    http.addHeader("Content-Type", "application/json");

    // Préparation des données JSON
    String jsonPayload = "{\"temperature\": " + String(temperature) + ", \"id_capteur\": 1}";

    // Requête POST
    int httpResponseCode = http.POST(jsonPayload);
    if (httpResponseCode > 0) {
      Serial.println("Données envoyées avec succès !");
      String response = http.getString();
      Serial.println("Réponse du serveur : " + response);
    } else {
      Serial.println("Erreur lors de l'envoi des données : " + String(httpResponseCode));
    }
    http.end();
  } else {
    Serial.println("WiFi déconnecté. Reconnexion...");
    WiFi.begin(ssid, password); // Tentative de reconnexion
  }

  // Attente avant le prochain envoi
  delay(6000); // 1 minute
}
