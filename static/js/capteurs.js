async function fetchCapteurs() {
    try {
        const response = await fetch("/api/Capteurs");
        if (!response.ok) throw new Error("Erreur lors de la récupération des capteurs");

        const capteurs = await response.json();
        const tableBody = document.getElementById("capteursTableBody");

        // Vider le tableau avant d'ajouter de nouvelles lignes
        tableBody.innerHTML = "";

        // Remplir le tableau avec les données récupérées
        capteurs.forEach(capteur => {
            const etatClass = capteur.etat === "Actif" ? "etat-actif" : "etat-inactif";

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${capteur.id_capteur}</td>
                <td>${capteur.id_type}</td>
                <td>${capteur.reference_commerciale}</td>
                <td>${capteur.id_piece}</td>
                <td>${capteur.port_communication}</td>
                <td>${new Date(capteur.date_insertion).toLocaleString()}</td>
                <td class="${etatClass}">${capteur.etat}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Erreur :", error.message);
    }
}

// Charger les données au démarrage
fetchCapteurs();
