document.addEventListener("DOMContentLoaded", () => {
    const capteursTable = document.getElementById("capteursTable");
    const addCapteurForm = document.getElementById("addCapteurForm");

    // Charger les capteurs/actionneurs
    async function loadCapteurs() {
        try {
            const response = await fetch("/api/Capteurs");
            if (!response.ok) throw new Error("Erreur lors du chargement des capteurs");
            const capteurs = await response.json();

            capteursTable.innerHTML = "";
            capteurs.forEach(capteur => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${capteur.id_capteur}</td>
                    <td>${capteur.id_type}</td>
                    <td>${capteur.reference_commerciale}</td>
                    <td>${capteur.id_piece}</td>
                    <td>${capteur.port_communication}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editCapteur(${capteur.id_capteur})">Modifier</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteCapteur(${capteur.id_capteur})">Supprimer</button>
                    </td>
                `;
                capteursTable.appendChild(row);
            });
        } catch (error) {
            console.error("Erreur :", error);
        }
    }

    // Ajouter un capteur/actionneur
    addCapteurForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const newCapteur = {
            id_type: document.getElementById("addType").value,
            reference_commerciale: document.getElementById("addReference").value,
            id_piece: document.getElementById("addPiece").value,
            port_communication: document.getElementById("addPort").value,
        };

        try {
            const response = await fetch("/api/Capteurs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newCapteur),
            });
            if (!response.ok) throw new Error("Erreur lors de l'ajout du capteur");
            loadCapteurs();
            addCapteurForm.reset();
        } catch (error) {
            console.error("Erreur :", error);
        }
    });

    // Supprimer un capteur/actionneur
    async function deleteCapteur(id) {
        try {
            const response = await fetch(`/api/Capteurs/${id}`, { method: "DELETE" });
            if (!response.ok) throw new Error("Erreur lors de la suppression");
            loadCapteurs();
        } catch (error) {
            console.error("Erreur :", error);
        }
    }

    // Charger les capteurs/actionneurs au chargement de la page
    loadCapteurs();
});
